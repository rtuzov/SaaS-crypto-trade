import { Swiper, SwiperSlide } from 'swiper/react'
import { Autoplay, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'

const screenshots = [
  {
    src: '/screenshots/dashboard.png',
    alt: 'Dashboard'
  },
  {
    src: '/screenshots/trade.png',
    alt: 'Trade Terminal'
  },
  {
    src: '/screenshots/analytics.png',
    alt: 'Analytics'
  }
]

export function Screenshots() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          Скриншоты интерфейса
        </h2>
        
        <Swiper
          modules={[Autoplay, Pagination]}
          spaceBetween={30}
          slidesPerView={1}
          pagination={{ clickable: true }}
          autoplay={{
            delay: 3000,
            disableOnInteraction: false
          }}
          breakpoints={{
            640: {
              slidesPerView: 2
            },
            1024: {
              slidesPerView: 3
            }
          }}
          className="w-full"
        >
          {screenshots.map((screenshot) => (
            <SwiperSlide key={screenshot.alt}>
              <div className="relative aspect-video rounded-lg overflow-hidden shadow-lg">
                <img
                  src={screenshot.src}
                  alt={screenshot.alt}
                  className="w-full h-full object-cover"
                />
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </section>
  )
} 