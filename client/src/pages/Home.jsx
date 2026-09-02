import React from 'react'
import Banner from '../components/home/Banner'
import HeroSection from '../components/home/HeroSection'
import Features from '../components/home/Features'
import Testimonial from '../components/home/Testimonial'
import CallToAction from '../components/home/CallToAction'
import Footer from '../components/home/Footer'

function Home() {
  return (
    <>
      <Banner />
      <HeroSection />
      <Features />
      <Testimonial />
      <CallToAction />
      <Footer />
    </>
  )
}

export default Home
