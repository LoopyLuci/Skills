# Per-category audio buses, and other runtime-property settings

## Why a shared sink makes a bus setting inert

A `rodio::Sink` carries **one** volume for everything appended to it. So

```rust
sink.set_volume(master * sfx);   // every sound
```

makes a music bus structurally unreachable: the `volume_music` setting saves,
reads back, appears in the settings UI, and changes nothing audible. This is the
same defect shape as an unwired UI control — the value is written and read by the
config layer, and nothing consumes it at the point that matters.

## The fix

Give each playback its own child sink of the mixer, and compute the level at play
time:

```rust
let bus = match category {
    SoundCategory::Music => self.config.music_volume,
    _ => self.config.sfx_volume,
};
let own = file_info.map(|s| s.volume).unwrap_or(1.0);

let voice = rodio::Sink::try_new(handle)?;          // handle: &OutputStreamHandle
voice.set_volume((self.config.master_volume * bus * own).clamp(0.0, 1.0));
voice.append(source);
voice.detach();                                      // outlives this scope
```

Honour the sound's own level too, or a deliberately quiet sound becomes as loud
as everything else once the bus is applied.

## rodio 0.17 API, each item a compile error otherwise

- No `Sink::new(&sink)` and no `Sink::mixer()`. Build from a stream handle:
  `rodio::Sink::try_new(&handle) -> Result<Sink, PlayError>`.
- No `OutputStreamHandle::try_default()`. Use
  `rodio::OutputStream::try_default() -> Result<(OutputStream, OutputStreamHandle), StreamError>`.
- `SoundCategory` needs `Copy` to read a category out of a map without cloning
  the whole `AudioFile`.
- **Store the handle on the struct.** Sinks attach to the handle, so dropping it
  silences playback; and opening an output device per sound is slow and fails on
  a busy device. Cache it behind `Option<...>` and open once.

## Test the arithmetic, not the playback

Tests construct the audio system without a device, so a playback-path test proves
nothing about which bus a sound used. Extract the bus choice as a pure function
and test it directly:

```rust
fn effective_bus(config: &AudioConfig, category: SoundCategory) -> f32 {
    match category {
        SoundCategory::Music => config.music_volume,
        _ => config.sfx_volume,
    }
}
```

Then assert: the two buses are independent; values clamp into `0.0..=1.0` at both
ends; and **only** `Music` takes the music bus. That last assertion is the one
that would have caught the original bug.

## The general shape

Any setting whose effect is applied at a single shared point (one sink, one
window style, one renderer) is inert if that point cannot distinguish the values
it is supposed to honour. Before wiring such a setting, check the application
point has enough information to vary its output per value — otherwise the setting
needs the application point reworked first, not just a reader added.