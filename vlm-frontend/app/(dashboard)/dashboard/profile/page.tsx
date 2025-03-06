"use client"

import { useState } from "react"
import { useSelector } from "react-redux"
import { useTheme } from "next-themes"
import { Check, ChevronDown } from "lucide-react"
import { RootState } from "@/lib/redux/store"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"

const themes = [
  {
    name: "Zinc",
    value: "zinc",
  },
  {
    name: "Slate",
    value: "slate",
  },
  {
    name: "Stone",
    value: "stone",
  },
  {
    name: "Gray",
    value: "gray",
  },
  {
    name: "Neutral",
    value: "neutral",
  },
]

export default function ProfilePage() {
  const user = useSelector((state: RootState) => state.auth.user)
  const { theme, setTheme } = useTheme()
  const [selectedColor, setSelectedColor] = useState("neutral")

  const handleThemeChange = (value: string) => {
    setTheme(value)
    toast.success(`Theme updated to ${value} mode`)
  }

  const handleColorChange = (value: string) => {
    setSelectedColor(value)
    toast.success(`Color scheme updated to ${value}`)
    // Here you would typically update the theme in your CSS variables
  }

  return (
    <div className='space-y-8'>
      <div>
        <h1 className='text-3xl font-bold'>Profile Settings</h1>
        <p className='text-muted-foreground'>
          Manage your account settings and set your preferences.
        </p>
      </div>

      <div className='grid gap-6'>
        <Card>
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>Update your personal details.</CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div className='grid gap-2'>
              <Label>Display Name</Label>
              <p className='text-lg font-medium'>{user?.displayName}</p>
            </div>
            <div className='grid gap-2'>
              <Label>Email</Label>
              <p className='text-lg font-medium'>{user?.email}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Appearance</CardTitle>
            <CardDescription>
              Customize the appearance of the app. Choose a theme and color
              scheme that suits you.
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-6'>
            <div className='space-y-4'>
              <Label>Theme Mode</Label>
              <RadioGroup
                defaultValue={theme}
                onValueChange={handleThemeChange}
                className='grid grid-cols-3 gap-4'
              >
                <Label
                  htmlFor='light'
                  className='flex cursor-pointer flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground [&:has([data-state=checked])]:border-primary'
                >
                  <RadioGroupItem
                    value='light'
                    id='light'
                    className='sr-only'
                  />
                  <span>Light</span>
                </Label>
                <Label
                  htmlFor='dark'
                  className='flex cursor-pointer flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground [&:has([data-state=checked])]:border-primary'
                >
                  <RadioGroupItem value='dark' id='dark' className='sr-only' />
                  <span>Dark</span>
                </Label>
                <Label
                  htmlFor='system'
                  className='flex cursor-pointer flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground [&:has([data-state=checked])]:border-primary'
                >
                  <RadioGroupItem
                    value='system'
                    id='system'
                    className='sr-only'
                  />
                  <span>System</span>
                </Label>
              </RadioGroup>
            </div>

            <Separator />

            <div className='space-y-4'>
              <Label>Color Scheme</Label>
              <Select value={selectedColor} onValueChange={handleColorChange}>
                <SelectTrigger className='w-[200px]'>
                  <SelectValue placeholder='Select a color' />
                </SelectTrigger>
                <SelectContent>
                  {themes.map((theme) => (
                    <SelectItem key={theme.value} value={theme.value}>
                      {theme.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
            <CardDescription>
              Manage your notification and display preferences.
            </CardDescription>
          </CardHeader>
          <CardContent>{/* Add more preference settings here */}</CardContent>
        </Card>
      </div>
    </div>
  )
}
