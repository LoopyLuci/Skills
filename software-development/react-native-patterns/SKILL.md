---
name: react-native-patterns
description: "Use when building mobile apps with React Native."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [React-Native, mobile, JavaScript, TypeScript, Expo, native-modules]
    related_skills: [flutter-mobile-development, swiftui-ios-development, kotlin-android-development, frontend-bootstrap]
---

# React Native Patterns

Building cross-platform mobile apps with React Native — from component architecture and navigation through state management, native modules, and performance optimization.

## When to Use

- Building iOS/Android apps with React/TypeScript
- Using Expo for rapid development
- Implementing native modules for platform-specific features
- State management with Redux, Zustand, or Jotai

## React Native Setup

```typescript
// Navigation pattern with Expo Router
import { Stack, Link } from 'expo-router';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="profile/[id]" options={{ title: 'Profile' }} />
    </Stack>
  );
}

// State management with Zustand
import { create } from 'zustand';
interface Store { count: number; increment: () => void; }
const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
}));

// Native module bridge (iOS)
// AppModule.m
/*
#import <React/RCTBridgeModule.h>
@interface CalendarModule : NSObject <RCTBridgeModule>
@end
*/
```

## Verification Checklist

- [ ] Project setup (Expo or React Native CLI)
- [ ] Navigation configured (Expo Router or React Navigation)
- [ ] State management chosen
- [ ] Native modules bridge for platform features
- [ ] Performance: FlatList, image caching, Hermes engine
- [ ] Platform-specific code with .ios/.android extensions
- [ ] OTA updates (Expo Update or CodePush)
- [ ] App store deployment checklist prepared
