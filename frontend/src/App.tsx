import { useEffect, useMemo, useState } from 'react'
import { ArrowRight, Clock, Menu, X } from 'lucide-react'
import { Shader, ChromaFlow, FilmGrain, FlutedGlass, Swirl } from 'shaders/react'

const smallImage =
  'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090123_74be96d4-9c1b-40cf-932a-96f4f4babed3.png&w=1280&q=85'

const largeImage =
  'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090133_c157d30b-a99a-4477-bec1-a446149ec3f2.png&w=1280&q=85'

function useLondonTime() {
  const [now, setNow] = useState(() => new Date())

  useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 1000)
    return () => window.clearInterval(timer)
  }, [])

  return useMemo(
    () =>
      new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Europe/London',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }).format(now),
    [now]
  )
}

function RollingText({ children }: { children: string }) {
  return (
    <span className="block h-[20px] overflow-hidden">
      <span className="flex flex-col transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-translate-y-1/2">
        <span>{children}</span>
        <span>{children}</span>
      </span>
    </span>
  )
}

function PartnerIcon() {
  return (
    <svg className="h-5 w-5 fill-current text-[#E8704E] sm:h-6 sm:w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" aria-hidden="true">
      <path d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z" />
    </svg>
  )
}

function MobileMenu({ open, onClose, time }: { open: boolean; onClose: () => void; time: string }) {
  return (
    <div className={`fixed inset-0 z-50 bg-black/60 transition-opacity duration-300 md:hidden ${open ? 'opacity-100' : 'pointer-events-none opacity-0'}`}>
      <div className={`absolute inset-x-0 bottom-0 mx-3 mb-3 rounded-2xl bg-white p-5 shadow-2xl transition-transform duration-500 ease-[cubic-bezier(0.32,0.72,0,1)] ${open ? 'translate-y-0' : 'translate-y-full'}`}>
        <div className="mb-8 flex items-center justify-between">
          <span className="rounded-full bg-gray-100 px-3 py-2 text-[13px] text-gray-600">
            {time} in London
          </span>
          <button className="grid h-10 w-10 place-items-center rounded-full bg-gray-900 text-white" onClick={onClose} aria-label="Close menu">
            <X size={18} />
          </button>
        </div>
        <nav className="grid gap-4 text-[28px] font-medium leading-8 text-gray-900">
          {['Projects', 'Studio', 'Journal', 'Connect'].map((item) => (
            <a key={item} href={`#${item.toLowerCase()}`} onClick={onClose}>
              {item}
            </a>
          ))}
        </nav>
        <button className="group mt-10 flex w-full items-center justify-between rounded-full bg-[#F26522] py-2 pl-5 pr-2 text-[13px] font-medium leading-[14px] text-white">
          <RollingText>Start a project</RollingText>
          <span className="grid h-8 w-8 place-items-center rounded-full bg-white text-[#F26522] transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-rotate-45">
            <ArrowRight size={16} />
          </span>
        </button>
      </div>
    </div>
  )
}

function Hero() {
  const time = useLondonTime()
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <section className="relative flex min-h-screen flex-col overflow-hidden bg-[#EFEFEF]">
      <div className="pointer-events-none absolute inset-0 z-10">
        <Shader className="h-full w-full">
          <Swirl colorA="#ffffff" colorB="#f0f0f0" detail={1.7} />
          <ChromaFlow baseColor="#ffffff" downColor="#ff5f03" leftColor="#ff5f03" rightColor="#ff5f03" upColor="#ff5f03" momentum={13} radius={3.5} />
          <FlutedGlass aberration={0.61} angle={31} frequency={8} highlight={0.12} highlightSoftness={0} lightAngle={-90} refraction={4} shape="rounded" softness={1} speed={0.15} />
          <FilmGrain strength={0.05} />
        </Shader>
      </div>

      <header className="relative z-20 mx-auto w-full max-w-[1440px] p-2 sm:p-3">
        <div className="flex items-center justify-between rounded-full bg-white p-[5px]">
          <div className="flex items-center gap-6">
            <div className="grid h-9 w-9 place-items-center rounded-full bg-gray-900 text-[10px] font-bold leading-[11px] tracking-tight text-white sm:h-10 sm:w-10">
              GV
            </div>
            <nav className="hidden items-center gap-6 text-[14px] text-gray-900 md:flex">
              {['Projects', 'Studio', 'Journal', 'Connect'].map((item) => (
                <a className="transition-colors duration-300 hover:text-gray-500" href={`#${item.toLowerCase()}`} key={item}>
                  {item}
                </a>
              ))}
            </nav>
          </div>

          <div className="hidden items-center gap-5 md:flex">
            <span className="hidden text-[13px] text-gray-600 lg:inline">Taking on event pilots for Q1 2026</span>
            <span className="flex items-center gap-1.5 text-[13px] text-gray-600">
              <Clock size={14} />
              {time} in London
            </span>
            <button className="group flex items-center gap-3 rounded-full bg-gray-900 py-2 pl-5 pr-2 text-[13px] font-medium text-white">
              <RollingText>Book a strategy call</RollingText>
              <span className="grid h-6 w-6 place-items-center rounded-full bg-white text-gray-900 transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-rotate-45">
                <ArrowRight size={14} />
              </span>
            </button>
          </div>

          <button className="grid h-9 w-16 place-items-center rounded-full bg-gray-900 text-white md:hidden" onClick={() => setMenuOpen(true)} aria-label="Open menu">
            <Menu size={18} />
          </button>
        </div>
      </header>

      <MobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} time={time} />

      <div className="flex-1" />

      <div className="relative z-20 mx-auto w-full max-w-[1440px] px-5 pb-14 sm:px-8 sm:pb-16 lg:px-12 lg:pb-20">
        <p className="mb-5 text-[13px] leading-[14px] tracking-wide text-gray-900 sm:mb-8">GuestVision AI</p>
        <h1 className="text-[clamp(1.75rem,7vw,4.2rem)] font-medium leading-[1.08] tracking-[-0.03em] text-gray-900 sm:text-[clamp(2.5rem,5vw,4.2rem)]">
          We craft intelligent check-in<span className="sm:hidden"> </span><br className="hidden sm:block" />
          experiences for events ready<span className="sm:hidden"> </span><br className="hidden sm:block" />
          to run faster at every gate.
        </h1>
        <div className="mt-8 flex flex-col gap-4 sm:mt-12 sm:flex-row sm:gap-5">
          <button className="group flex w-fit items-center gap-4 rounded-full bg-[#F26522] py-2 pl-5 pr-2 text-[13px] font-medium leading-[14px] text-white transition-colors duration-300 hover:bg-[#e05a1a] sm:pl-6">
            <RollingText>Start a project</RollingText>
            <span className="grid h-7 w-7 place-items-center rounded-full bg-white text-[#F26522] transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-rotate-45 sm:h-8 sm:w-8">
              <ArrowRight size={16} />
            </span>
          </button>
          <div className="flex w-fit items-center gap-3 rounded-[4px] bg-white px-3 py-2 shadow-[0_2px_8px_rgba(0,0,0,0.08)] transition-shadow hover:shadow-[0_4px_16px_rgba(0,0,0,0.12)] sm:px-4">
            <PartnerIcon />
            <span className="text-[13px] font-medium leading-[14px] text-gray-900">Certified Partner</span>
            <span className="rounded bg-gray-900 px-1.5 py-0.5 text-[10px] leading-[11px] text-white sm:px-2">Featured</span>
          </div>
        </div>
      </div>
    </section>
  )
}

function BadgeRow({ number, label, muted = false }: { number: string; label: string; muted?: boolean }) {
  return (
    <div className="mb-6 flex items-center gap-3 px-5 sm:mb-8 sm:px-8 lg:px-12">
      <span className="grid h-6 w-6 place-items-center rounded-full bg-gray-900 text-[11px] font-semibold leading-3 text-white sm:h-7 sm:w-7">{number}</span>
      <span className={`rounded-full border px-3 py-1 text-[12px] font-medium leading-[13px] sm:px-4 sm:py-1.5 ${muted ? 'border-gray-300' : 'border-gray-200'}`}>{label}</span>
    </div>
  )
}

function About() {
  return (
    <section id="studio" className="overflow-hidden bg-white pb-12 pt-16 sm:pb-16 sm:pt-20 lg:pb-24 lg:pt-32">
      <div className="mx-auto max-w-[1440px]">
        <BadgeRow number="1" label="Introducing GuestVision" />
        <h2 className="mb-12 px-5 text-[clamp(1.5rem,4vw,3.2rem)] font-medium leading-[1.12] tracking-[-0.02em] text-gray-900 sm:mb-16 sm:px-8 lg:mb-28 lg:px-12">
          Strategy-led AI, delivering<span className="sm:hidden"> </span><br className="hidden sm:block" />
          results at the door and beyond.
        </h2>

        <div className="px-5 sm:px-8 lg:hidden">
          <p className="max-w-xl text-[15px] font-medium leading-[1.6] text-gray-900">
            Through real-time recognition, QR fallback, and event analytics we help growing teams realize their operational full potential.
          </p>
          <button className="group mt-6 flex w-fit items-center gap-4 rounded-full bg-[#F26522] py-2 pl-5 pr-2 text-[13px] font-medium leading-[14px] text-white transition-colors hover:bg-[#e05a1a]">
            <RollingText>About our studio</RollingText>
            <span className="grid h-8 w-8 place-items-center rounded-full bg-white text-[#F26522] transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-rotate-45">
              <ArrowRight size={16} />
            </span>
          </button>
          <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:gap-5">
            <img className="aspect-[438/346] w-full rounded-xl object-cover sm:w-[45%] sm:rounded-2xl" src={smallImage} alt="GuestVision event command surface" />
            <img className="aspect-[900/600] w-full rounded-xl object-cover sm:w-[55%] sm:rounded-2xl" src={largeImage} alt="GuestVision operator workflow" />
          </div>
        </div>

        <div className="hidden grid-cols-[26%_1fr_48%] items-end gap-6 px-12 lg:grid xl:gap-8">
          <img className="aspect-[438/346] w-full self-end rounded-2xl object-cover" src={smallImage} alt="GuestVision event command surface" />
          <div className="self-start justify-self-end">
            <p className="whitespace-nowrap text-[16px] font-medium leading-[1.65] text-gray-900">
              Through real-time recognition,<br />
              QR fallback and event analytics<br />
              we help teams move faster.
            </p>
            <button className="group mt-8 flex w-fit items-center gap-4 rounded-full bg-[#F26522] py-2 pl-6 pr-2 text-[13px] font-medium leading-[14px] text-white transition-colors hover:bg-[#e05a1a]">
              <RollingText>About our studio</RollingText>
              <span className="grid h-8 w-8 place-items-center rounded-full bg-white text-[#F26522] transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)] group-hover:-rotate-45">
                <ArrowRight size={16} />
              </span>
            </button>
          </div>
          <img className="aspect-[3/2] w-full self-end rounded-2xl object-cover" src={largeImage} alt="GuestVision operator workflow" />
        </div>
      </div>
    </section>
  )
}

function CaseStudies() {
  return (
    <section id="projects" className="bg-[#F5F5F5] pb-16 pt-16 sm:pb-20 sm:pt-20 lg:pb-28 lg:pt-28">
      <div className="mx-auto max-w-[1440px]">
        <BadgeRow number="2" label="Featured client work" muted />
        <h2 className="mb-10 px-5 text-[clamp(1.75rem,7vw,4.2rem)] font-medium leading-[1.08] tracking-[-0.03em] text-gray-900 sm:mb-14 sm:px-8 sm:text-[clamp(2.5rem,5vw,4.2rem)] lg:mb-16 lg:px-12">
          Our projects
        </h2>
        <div className="grid grid-cols-1 gap-5 px-5 sm:gap-6 sm:px-8 md:grid-cols-2 lg:gap-7 lg:px-12">
          <article>
            <div className="group relative aspect-[329/246] cursor-pointer overflow-hidden rounded-2xl bg-[#1a1d2e]">
              <video className="h-full w-full object-cover" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260516_122702_390f5305-8719-41d5-ae80-d23ab3796c28.mp4" autoPlay muted loop playsInline />
              <button className="absolute bottom-4 left-4 flex h-9 w-9 items-center justify-end gap-2 overflow-hidden rounded-full bg-white px-3 text-gray-900 transition-all duration-300 ease-in-out group-hover:w-[148px]">
                <span className="whitespace-nowrap text-[13px] font-medium opacity-0 transition-opacity delay-100 group-hover:opacity-100">Learn more</span>
                <svg className="h-[14px] w-[14px] shrink-0 -rotate-45 transition-transform duration-300 group-hover:rotate-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                </svg>
              </button>
            </div>
            <p className="mt-4 text-[13px] leading-relaxed text-gray-600">Winner of Site of the Month 2025 - an interactive 3D showcase driving record engagement</p>
            <h3 className="mt-1 text-[14px] font-semibold leading-[15px] text-gray-900">Narrativ</h3>
          </article>

          <article>
            <div className="group relative aspect-square cursor-pointer overflow-hidden rounded-2xl bg-[#6b6b6b]">
              <video className="h-full w-full object-cover" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260516_123323_f909c2b8-ff6c-4edf-882b-8ebcdbe389b5.mp4" autoPlay muted loop playsInline />
              <button className="absolute bottom-4 left-4 flex h-9 w-9 items-center justify-end gap-2 overflow-hidden rounded-full bg-gray-900 px-3 text-white transition-all duration-300 ease-in-out group-hover:w-[168px]">
                <span className="whitespace-nowrap text-[13px] font-medium opacity-0 transition-opacity delay-100 group-hover:opacity-100">View case study</span>
                <ArrowRight className="shrink-0 -rotate-45 transition-transform duration-300 group-hover:rotate-0" size={14} />
              </button>
            </div>
            <p className="mt-4 text-[13px] leading-relaxed text-gray-600">Transforming a dated platform into a conversion-focused brand experience</p>
            <h3 className="mt-1 text-[14px] font-semibold leading-[15px] text-gray-900">Luminar</h3>
          </article>
        </div>
      </div>
    </section>
  )
}

export default function App() {
  return (
    <>
      <Hero />
      <About />
      <CaseStudies />
    </>
  )
}
