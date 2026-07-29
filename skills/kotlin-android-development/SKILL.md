---
name: kotlin-android-development
description: "Use when building Android apps with Kotlin."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Kotlin, Android, Jetpack-Compose, coroutines, MVVM, Room]
    related_skills: [flutter-mobile-development, react-native-patterns, swiftui-ios-development, frontend-bootstrap]
---

# Kotlin Android Development

Building Android apps with Kotlin — from Jetpack Compose and coroutines through MVVM architecture, Room database, and Play Store deployment.

## When to Use

- Building native Android applications
- Modern UI with Jetpack Compose
- Reactive UIs with StateFlow and coroutines
- Offline-first with Room database

## Kotlin Android Patterns

```kotlin
// MVVM with Jetpack Compose
class MainViewModel : ViewModel() {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()
    
    init { viewModelScope.launch { loadUsers() } }
    
    fun loadUsers() {
        viewModelScope.launch {
            _users.value = repository.getUsers()
        }
    }
}

@Composable
fun UserListScreen(viewModel: MainViewModel) {
    val users by viewModel.users.collectAsState()
    
    LazyColumn {
        items(users) { user ->
            UserCard(user = user)
        }
    }
}

// Room database
@Entity
data class User(
    @PrimaryKey val id: String,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    suspend fun getAll(): List<User>
}
```

## Verification Checklist

- [ ] Architecture chosen (MVVM, MVI, or Clean Architecture)
- [ ] UI built with Jetpack Compose
- [ ] Navigation Component for screen routing
- [ ] Room database for local persistence
- [ ] Coroutines + Flow for async operations
- [ ] Dependency injection (Hilt or Koin)
- [ ] Retrofit/Ktor for networking
- [ ] Testing (JUnit, Compose UI tests, MockK)
- [ ] Google Play deployment checklist ready
