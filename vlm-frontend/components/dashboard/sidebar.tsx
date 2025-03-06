"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useDispatch, useSelector } from "react-redux"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  BarChart3,
  Calendar,
  Camera,
  Home,
  LogOut,
  Settings,
  User,
} from "lucide-react"
import { logoutUser } from "@/lib/redux/features/authSlice"
import { RootState } from "@/lib/redux/store"
import { ThemeSwitcher } from "./theme-switcher"

const sidebarItems = [
  { name: "Dashboard", icon: Home, href: "/dashboard" },
  { name: "Scan Label", icon: Camera, href: "/dashboard/scan" },
  { name: "Analytics", icon: BarChart3, href: "/dashboard/analytics" },
  { name: "Calendar", icon: Calendar, href: "/dashboard/calendar" },
]

export function Sidebar() {
  const pathname = usePathname()
  const dispatch = useDispatch()
  const user = useSelector((state: RootState) => state.auth.user)

  const handleLogout = () => {
    dispatch(logoutUser())
  }

  return (
    <div className='flex h-full w-[240px] flex-col border-r bg-card'>
      <div className='flex items-center justify-between p-6'>
        <div>
          <h2 className='text-lg font-semibold'>NutriScan</h2>
          <p className='text-sm text-muted-foreground'>
            Welcome, {user?.displayName}
          </p>
        </div>
        <ThemeSwitcher />
      </div>
      <ScrollArea className='flex-1 px-3'>
        <div className='space-y-1'>
          {sidebarItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <Button
                variant={pathname === item.href ? "secondary" : "ghost"}
                className={cn("w-full justify-start")}
              >
                <item.icon className='mr-2 h-4 w-4' />
                {item.name}
              </Button>
            </Link>
          ))}
        </div>
      </ScrollArea>
      <div className='p-6'>
        <Button
          variant='ghost'
          className='w-full justify-start'
          onClick={handleLogout}
        >
          <LogOut className='mr-2 h-4 w-4' />
          Logout
        </Button>
      </div>
    </div>
  )
}
