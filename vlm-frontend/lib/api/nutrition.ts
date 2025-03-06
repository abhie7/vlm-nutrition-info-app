import api from "./axios"

interface NutritionResponse {
  success: boolean
  data?: any
  message?: string
}

export const nutritionApi = {
  analyzeLabel: async (payload: {
    user_uuid: string
    food_name: string
    meal_type: string
    tags: string[]
    image_url: string
  }): Promise<NutritionResponse> => {
    try {
      const response = await api.post("/nutrition/analyze", payload)
      return {
        success: true,
        data: response.data,
      }
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Failed to analyze label",
      }
    }
  },

  getDailyLogs: async (date: string): Promise<NutritionResponse> => {
    try {
      const response = await api.get(`/nutrition/logs/${date}`)
      return {
        success: true,
        data: response.data,
      }
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || "Failed to fetch daily logs",
      }
    }
  },
}
