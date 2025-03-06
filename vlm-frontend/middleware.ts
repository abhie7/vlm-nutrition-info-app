import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // const authToken = request.cookies.get("auth_token")
  // const { pathname } = request.nextUrl

  // Public routes that don't require authentication
  const publicRoutes = ["/", "/login", "/register", "/forgot-password"]

  // Protected routes that require authentication
  const protectedRoutes = ["/dashboard", "/profile", "/settings"]

  // Check if the path starts with any protected route
  // const isProtectedRoute = protectedRoutes.some((route) =>
  //   pathname.startsWith(route)
  // )

  // Check if the path is a public route
  // const isPublicRoute = publicRoutes.includes(pathname)

  // If trying to access protected route without auth, redirect to login
  // if (isProtectedRoute && !authToken) {
  //   return NextResponse.redirect(new URL("/login", request.url))
  // }

  // If trying to access auth routes while authenticated, redirect to dashboard
  // if (isPublicRoute && authToken) {
  //   return NextResponse.redirect(new URL("/dashboard", request.url))
  // }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
}
