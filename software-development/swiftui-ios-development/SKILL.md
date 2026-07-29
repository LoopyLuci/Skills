---
name: swiftui-ios-development
description: "Use when building iOS apps with SwiftUI."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [SwiftUI, iOS, Swift, Apple, Combine, CoreData, SwiftData]
    related_skills: [flutter-mobile-development, react-native-patterns, kotlin-android-development, webxr-ar-vr-development]
---

# SwiftUI iOS Development

Building iOS apps with SwiftUI — from view composition and data flow through navigation, state management, networking, and App Store deployment.

## When to Use

- Building iOS, iPadOS, macOS, watchOS apps
- Implementing SwiftUI declarative UI
- Managing state with @State, @Binding, @Observable
- Building with SwiftData or Core Data

## SwiftUI Patterns

```swift
import SwiftUI

// MVVM pattern with @Observable
@Observable
class TaskViewModel {
    var tasks: [Task] = []
    var isLoading = false
    
    func fetchTasks() async {
        isLoading = true
        // API call
        tasks = await api.fetchTasks()
        isLoading = false
    }
}

struct TaskListView: View {
    @State private var vm = TaskViewModel()
    
    var body: some View {
        NavigationStack {
            List(vm.tasks) { task in
                HStack {
                    Text(task.title)
                    Spacer()
                    Image(systemName: task.isDone ? "checkmark.circle.fill" : "circle")
                }
            }
            .navigationTitle("Tasks")
            .toolbar {
                ToolbarItem { Button("Add") { /* add task */ } }
            }
            .task { await vm.fetchTasks() }
        }
    }
}
```

## Verification Checklist

- [ ] Data flow pattern chosen (MVVM, TCA, or SwiftUI native)
- [ ] Navigation (NavigationStack, TabView, SplitView)
- [ ] State management (@State, @Observable, @Bindable)
- [ ] Persistence (SwiftData, CoreData, or UserDefaults)
- [ ] Networking (URLSession, async/await)
- [ ] Adaptability (iPad, Mac Catalyst, visionOS)
- [ ] Performance: LazyVStack, image caching, prefetching
- [ ] App Store Connect configuration ready
