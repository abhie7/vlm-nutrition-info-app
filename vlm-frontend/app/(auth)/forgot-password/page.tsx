"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import Link from "next/link"
import { Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { authApi } from "@/lib/api/auth"
import { toast } from "sonner"

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
})

export default function ForgotPasswordPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      setIsLoading(true)
      await authApi.forgotPassword(values.email)
      setIsSubmitted(true)
      toast.success("Password reset instructions sent to your email")
    } catch (error) {
      toast.error("Failed to send reset instructions. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className='space-y-6 text-center'>
        <h1 className='text-3xl font-bold'>Check Your Email</h1>
        <p className='text-muted-foreground'>
          We've sent password reset instructions to your email address.
        </p>
        <div className='space-y-2'>
          <p className='text-sm text-muted-foreground'>
            Didn't receive the email?{" "}
            <Button
              variant='link'
              className='p-0 text-primary'
              onClick={() => setIsSubmitted(false)}
            >
              Try again
            </Button>
          </p>
          <p className='text-sm text-muted-foreground'>
            Or{" "}
            <Link href='/login' className='text-primary hover:underline'>
              return to login
            </Link>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className='space-y-6'>
      <div className='space-y-2 text-center'>
        <h1 className='text-3xl font-bold'>Forgot Password</h1>
        <p className='text-muted-foreground'>
          Enter your email address and we'll send you instructions to reset your
          password
        </p>
      </div>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4'>
          <FormField
            control={form.control}
            name='email'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder='you@example.com' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type='submit' className='w-full' disabled={isLoading}>
            {isLoading && <Loader2 className='mr-2 h-4 w-4 animate-spin' />}
            Send Reset Instructions
          </Button>
        </form>
      </Form>
      <div className='text-center text-sm'>
        <p className='text-muted-foreground'>
          Remember your password?{" "}
          <Link href='/login' className='text-primary hover:underline'>
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
