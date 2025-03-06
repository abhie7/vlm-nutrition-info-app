import { configureStore } from "@reduxjs/toolkit"
import authReducer from "./features/authSlice"
import nutritionReducer from "./features/nutritionSlice"

export const store = configureStore({
  reducer: {
    auth: authReducer,
    nutrition: nutritionReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch