"use client"

import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { RootState } from "@/lib/redux/store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Camera, Plus } from "lucide-react"
import { useRouter } from "next/navigation"
import { ScanDialog } from "@/components/scan-label/scan-dialog"

export default function DashboardPage() {
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const { dailyLogs, waterIntake } = useSelector(
    (state: RootState) => state.nutrition
  )

  return (
    <div className='space-y-8'>
      <div className='flex items-center justify-between'>
        <h1 className='text-3xl font-bold'>Dashboard</h1>
        <Button onClick={() => setOpen(true)}>
          <Camera className='mr-2 h-4 w-4' />
          Scan Label
        </Button>
      </div>

      <div className='grid gap-4 md:grid-cols-2 lg:grid-cols-4'>
        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>
              Total Calories Today
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>2,345</div>
            <p className='text-xs text-muted-foreground'>
              +20.1% from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>
              Protein Intake
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>65g</div>
            <p className='text-xs text-muted-foreground'>80% of daily goal</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>Water Intake</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>{waterIntake}ml</div>
            <Button
              variant='ghost'
              size='sm'
              className='mt-2'
              onClick={() => {}}
            >
              <Plus className='mr-2 h-4 w-4' />
              Add Water
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium'>Meals Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>{dailyLogs.length}</div>
            <p className='text-xs text-muted-foreground'>
              Last meal 2 hours ago
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Add more dashboard content here */}
    </div>
  )
}
