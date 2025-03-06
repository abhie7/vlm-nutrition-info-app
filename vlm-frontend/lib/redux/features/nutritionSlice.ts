import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface NutritionState {
  dailyLogs: any[]
  waterIntake: number
  loading: boolean
  currentScan: {
    image: string | null
    processing: boolean
    result: any | null
  }
}

const initialState: NutritionState = {
  dailyLogs: [],
  waterIntake: 0,
  loading: false,
  currentScan: {
    image: null,
    processing: false,
    result: null,
  },
}

const nutritionSlice = createSlice({
  name: "nutrition",
  initialState,
  reducers: {
    setDailyLogs: (state, action: PayloadAction<any[]>) => {
      state.dailyLogs = action.payload
    },
    updateWaterIntake: (state, action: PayloadAction<number>) => {
      state.waterIntake = action.payload
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setCurrentScan: (state, action: PayloadAction<Partial<NutritionState["currentScan"]>>) => {
      state.currentScan = { ...state.currentScan, ...action.payload }
    },
  },
})

export const { setDailyLogs, updateWaterIntake, setLoading, setCurrentScan } = nutritionSlice.actions
export default nutritionSlice.reducer