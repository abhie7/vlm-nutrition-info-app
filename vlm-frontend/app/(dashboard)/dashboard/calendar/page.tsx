"use client"

import { useState } from "react"
import { useSelector } from "react-redux"
import { format } from "date-fns"
import { Calendar as CalendarIcon } from "lucide-react"
import { RootState } from "@/lib/redux/store"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

const nutrientOptions = [
  { label: "Calories", value: "calories" },
  { label: "Protein", value: "protein" },
  { label: "Carbs", value: "carbs" },
  { label: "Fat", value: "fat" },
  { label: "Fiber", value: "fiber" },
  { label: "Sugar", value: "sugar" },
]

export default function CalendarPage() {
  const [date, setDate] = useState<Date>(new Date())
  const [selectedNutrient, setSelectedNutrient] = useState("calories")
  const dailyLogs = useSelector((state: RootState) => state.nutrition.dailyLogs)

  // Mock data for demonstration
  const selectedDateLogs = dailyLogs.filter(
    (log) =>
      format(new Date(log.created_at), "yyyy-MM-dd") ===
      format(date, "yyyy-MM-dd")
  )

  return (
    <div className='space-y-8'>
      <div className='flex items-center justify-between'>
        <div>
          <h1 className='text-3xl font-bold'>Nutrition Calendar</h1>
          <p className='text-muted-foreground'>
            Track your nutrition intake over time
          </p>
        </div>
        <div className='flex items-center space-x-2'>
          <Select value={selectedNutrient} onValueChange={setSelectedNutrient}>
            <SelectTrigger className='w-[180px]'>
              <SelectValue placeholder='Select nutrient' />
            </SelectTrigger>
            <SelectContent>
              {nutrientOptions.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant='outline'
                className='w-[240px] justify-start text-left font-normal'
              >
                <CalendarIcon className='mr-2 h-4 w-4' />
                {format(date, "PPP")}
              </Button>
            </PopoverTrigger>
            <PopoverContent className='w-auto p-0' align='start'>
              <Calendar
                mode='single'
                selected={date}
                onSelect={(date) => date && setDate(date)}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>

      <div className='grid gap-6'>
        <Card>
          <CardHeader>
            <CardTitle>Daily Overview</CardTitle>
            <CardDescription>
              Nutrition intake for {format(date, "MMMM d, yyyy")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {selectedDateLogs.length > 0 ? (
              <div className='space-y-4'>
                {selectedDateLogs.map((log, index) => (
                  <div
                    key={index}
                    className='flex items-center justify-between border-b pb-4 last:border-0 last:pb-0'
                  >
                    <div>
                      <p className='font-medium'>{log.food_name}</p>
                      <p className='text-sm text-muted-foreground'>
                        {log.meal_type} • {log.tags.join(", ")}
                      </p>
                    </div>
                    <div className='text-right'>
                      <p className='font-medium'>
                        {log.nutrient_info.total_calories} kcal
                      </p>
                      <p className='text-sm text-muted-foreground'>
                        {log.nutrient_info.nutrients.protein.amount}g protein
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className='text-center py-8'>
                <p className='text-muted-foreground'>
                  No nutrition data recorded for this date
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Additional cards for weekly/monthly trends could be added here */}
      </div>
    </div>
  )
}
