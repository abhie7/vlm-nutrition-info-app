import api from "./axios"

interface AuthResponse {
  success: boolean
  user?: {
    uuid: string
    email: string
    displayName: string
  }
  token?: string
  message?: string
}

export const authApi = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    try {
      const response = await api.post("/auth/login", { email, password })
      return response.data
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Login failed",
      }
    }
  },

  register: async (
    email: string,
    password: string,
    displayName: string
  ): Promise<AuthResponse> => {
    try {
      const response = await api.post("/auth/register", {
        email,
        password,
        displayName,
      })
      return response.data
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Registration failed",
      }
    }
  },

  forgotPassword: async (email: string): Promise<AuthResponse> => {
    try {
      const response = await api.post("/auth/forgot-password", { email })
      return response.data
    } catch (error: any) {
      return {
        success: false,
        message:
          error.response?.data?.message || "Failed to send reset instructions",
      }
    }
  },

  resetPassword: async (
    token: string,
    password: string
  ): Promise<AuthResponse> => {
    try {
      const response = await api.post("/auth/reset-password", {
        token,
        password,
      })
      return response.data
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Password reset failed",
      }
    }
  },

  validateToken: async (): Promise<AuthResponse> => {
    try {
      const response = await api.get("/auth/validate")
      return response.data
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Token validation failed",
      }
    }
  },
}
