// "use client"

// import { useEffect } from "react"
// import { useRouter } from "next/navigation"
// import { useSelector } from "react-redux"
// import { RootState } from "@/lib/redux/store"
// import { Sidebar } from "@/components/dashboard/sidebar"

// export default function DashboardLayout({
//   children,
// }: {
//   children: React.ReactNode
// }) {
//   const router = useRouter()
//   const { isAuthenticated } = useSelector((state: RootState) => state.auth)

//   useEffect(() => {
//     if (!isAuthenticated) {
//       router.push("/login")
//     }
//   }, [isAuthenticated, router])

//   if (!isAuthenticated) {
//     return null
//   }

//   return (
//     <div className='flex h-screen overflow-hidden'>
//       <Sidebar />
//       <main className='flex-1 overflow-y-auto bg-background'>
//         <div className='container mx-auto py-8'>{children}</div>
//       </main>
//     </div>
//   )
// }

"use client"

import { Sidebar } from "@/components/dashboard/sidebar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className='flex h-screen overflow-hidden'>
      <Sidebar />
      <main className='flex-1 overflow-y-auto bg-background'>
        <div className='container mx-auto py-8'>{children}</div>
      </main>
    </div>
  )
}
