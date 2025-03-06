import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"
import { authApi } from "@/lib/api/auth"
import Cookies from "js-cookie"

interface User {
  id: string
  email: string
  displayName: string
}

interface AuthState {
  isAuthenticated: boolean
  user: User | null
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
}

// Async thunks
export const loginUser = createAsyncThunk(
  "auth/login",
  async (
    { email, password }: { email: string; password: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await authApi.login(email, password)
      if (response.success) {
        Cookies.set("auth_token", response.token, { expires: 7 })
        return response.user
      }
      return rejectWithValue(response.message)
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || "Login failed")
    }
  }
)

export const registerUser = createAsyncThunk(
  "auth/register",
  async (
    {
      email,
      password,
      displayName,
    }: { email: string; password: string; displayName: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await authApi.register(email, password, displayName)
      if (response.success) {
        Cookies.set("auth_token", response.token, { expires: 7 })
        return response.user
      }
      return rejectWithValue(response.message)
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.message || "Registration failed"
      )
    }
  }
)

export const logoutUser = createAsyncThunk("auth/logout", async () => {
  Cookies.remove("auth_token")
  return null
})

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User | null>) => {
      state.isAuthenticated = !!action.payload
      state.user = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isAuthenticated = true
        state.user = action.payload
        state.loading = false
        state.error = null
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })

    // Register
    builder
      .addCase(registerUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.isAuthenticated = true
        state.user = action.payload
        state.loading = false
        state.error = null
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })

    // Logout
    builder.addCase(logoutUser.fulfilled, (state) => {
      state.isAuthenticated = false
      state.user = null
      state.loading = false
      state.error = null
    })
  },
})

export const { setUser, setError, clearError } = authSlice.actions
export default authSlice.reducer
