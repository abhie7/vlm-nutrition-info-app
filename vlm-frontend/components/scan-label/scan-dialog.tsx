"use client"

import { useState } from "react"
import { useSelector } from "react-redux"
import { useDropzone } from "react-dropzone"
import { Camera, Upload, X } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { RootState } from "@/lib/redux/store"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import { toast } from "sonner"
import Image from "next/image"

const formSchema = z.object({
  food_name: z.string().min(2, "Food name must be at least 2 characters"),
  meal_type: z.enum(["breakfast", "lunch", "dinner", "snack"]),
  tags: z.array(z.string()).min(1, "Select at least one tag"),
})

const mealTypes = [
  { value: "breakfast", label: "Breakfast", color: "bg-yellow-500" },
  { value: "lunch", label: "Lunch", color: "bg-green-500" },
  { value: "dinner", label: "Dinner", color: "bg-blue-500" },
  { value: "snack", label: "Snack", color: "bg-purple-500" },
]

const availableTags = [
  { value: "healthy", label: "Healthy", color: "bg-green-100 text-green-800" },
  { value: "spicy", label: "Spicy", color: "bg-red-100 text-red-800" },
  { value: "sweet", label: "Sweet", color: "bg-pink-100 text-pink-800" },
  { value: "salty", label: "Salty", color: "bg-blue-100 text-blue-800" },
  { value: "fatty", label: "Fatty", color: "bg-yellow-100 text-yellow-800" },
]

const loadingMessages = [
  "Having a glass of water while you wait?",
  "Time for a quick stretch!",
  "Remember to sit straight 🪑",
  "Breathe in, breathe out 🧘‍♀️",
  "Almost there! Stay hydrated 💧",
]

interface ScanDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ScanDialog({ open, onOpenChange }: ScanDialogProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0)
  const user = useSelector((state: RootState) => state.auth.user)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      food_name: "",
      meal_type: "snack",
      tags: [],
    },
  })

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "image/*": [".png", ".jpg", ".jpeg"],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0]
      setSelectedImage(file)
      setPreviewUrl(URL.createObjectURL(file))
    },
  })

  const handleCameraCapture = () => {
    // Implementation for camera capture
    toast.info("Camera capture coming soon!")
  }

  const uploadImage = async (file: File): Promise<string> => {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("upload_preset", "nutriscan")

    try {
      const response = await fetch(
        `https://api.cloudinary.com/v1_1/${process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME}/image/upload`,
        {
          method: "POST",
          body: formData,
        }
      )
      const data = await response.json()
      return data.secure_url
    } catch (error) {
      throw new Error("Failed to upload image")
    }
  }

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    if (!selectedImage || !user) return

    try {
      setIsUploading(true)
      // Rotate loading messages
      const interval = setInterval(() => {
        setLoadingMessageIndex((prev) => (prev + 1) % loadingMessages.length)
      }, 3000)

      const imageUrl = await uploadImage(selectedImage)

      const payload = {
        user_uuid: user.uuid,
        food_name: values.food_name,
        meal_type: values.meal_type,
        tags: values.tags,
        image_url: imageUrl,
      }

      // Send to backend
      // const response = await api.post("/nutrition/analyze", payload)

      clearInterval(interval)
      toast.success("Food label analyzed successfully!")
      onOpenChange(false)
    } catch (error) {
      toast.error("Failed to analyze food label")
    } finally {
      setIsUploading(false)
    }
  }

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    )
    form.setValue("tags", selectedTags)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className='sm:max-w-[800px]'>
        <DialogHeader>
          <DialogTitle>Scan Food Label</DialogTitle>
          <DialogDescription>
            Upload a photo of your food label or take a picture to analyze its
            nutritional content.
          </DialogDescription>
        </DialogHeader>

        <div className='grid gap-6 py-4 md:grid-cols-2'>
          <div className='space-y-4'>
            <div
              {...getRootProps()}
              className='border-2 border-dashed rounded-lg p-6 text-center hover:border-primary cursor-pointer'
            >
              <input {...getInputProps()} />
              {previewUrl ? (
                <div className='relative'>
                  <Image
                    src={previewUrl}
                    alt='Preview'
                    width={200}
                    height={200}
                    className='max-h-[200px] mx-auto rounded'
                  />
                  <Button
                    variant='ghost'
                    size='icon'
                    className='absolute top-0 right-0'
                    onClick={(e) => {
                      e.stopPropagation()
                      setSelectedImage(null)
                      setPreviewUrl(null)
                    }}
                  >
                    <X className='h-4 w-4' />
                  </Button>
                </div>
              ) : (
                <div className='space-y-2'>
                  <Upload className='h-8 w-8 mx-auto text-muted-foreground' />
                  <p>Drag & drop or click to upload</p>
                </div>
              )}
            </div>

            <div className='text-center'>
              <Button
                variant='outline'
                className='w-full'
                onClick={handleCameraCapture}
              >
                <Camera className='mr-2 h-4 w-4' />
                Take Photo
              </Button>
            </div>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4'>
              <FormField
                control={form.control}
                name='food_name'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Food Name</FormLabel>
                    <FormControl>
                      <Input placeholder='Enter food name' {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='meal_type'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Meal Type</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder='Select meal type' />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {mealTypes.map((type) => (
                          <SelectItem
                            key={type.value}
                            value={type.value}
                            className='flex items-center'
                          >
                            <div
                              className={`w-2 h-2 rounded-full mr-2 ${type.color}`}
                            />
                            {type.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='tags'
                render={() => (
                  <FormItem>
                    <FormLabel>Tags</FormLabel>
                    <div className='flex flex-wrap gap-2'>
                      {availableTags.map((tag) => (
                        <Badge
                          key={tag.value}
                          variant='outline'
                          className={`cursor-pointer ${
                            selectedTags.includes(tag.value)
                              ? tag.color
                              : "bg-transparent"
                          }`}
                          onClick={() => toggleTag(tag.value)}
                        >
                          {tag.label}
                        </Badge>
                      ))}
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button
                type='submit'
                className='w-full'
                disabled={isUploading || !selectedImage}
              >
                {isUploading ? (
                  <>
                    <LoadingSpinner className='mr-2' />
                    <AnimatePresence mode='wait'>
                      <motion.span
                        key={loadingMessageIndex}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.2 }}
                      >
                        {loadingMessages[loadingMessageIndex]}
                      </motion.span>
                    </AnimatePresence>
                  </>
                ) : (
                  "Analyze Label"
                )}
              </Button>
            </form>
          </Form>
        </div>
      </DialogContent>
    </Dialog>
  )
}
