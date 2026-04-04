<template>
  <div class="flex min-h-screen flex-col bg-(--page-bg) transition-colors duration-300">
    <SiteHeader />

    <main class="flex-1">
      <section
        ref="heroSectionRef"
        class="homepage-hero relative overflow-hidden px-0 py-20 sm:px-10 sm:py-30 lg:px-32"
        @pointermove="handlePointerMove"
        @pointerleave="resetPointerOffset"
      >
        <div
          class="homepage-hero__background"
          :class="{ 'homepage-hero__background--dark': isDark }"
          :style="backgroundStyle"
          aria-hidden="true"
        />

        <div class="relative z-10 mx-auto w-full max-w-7xl px-4 sm:px-6 md:px-10 lg:px-10">
          <h1
            class="text-4xl font-black uppercase leading-[1.06] tracking-[0.02em] text-(--text-hero) sm:text-7xl lg:text-7xl"
          >
            Тест по определению направления
          </h1>
          <p
            class="mt-6 text-base uppercase leading-snug tracking-[-0.02em] text-(--text-body) sm:mt-8 sm:text-2xl"
          >
            Прохождение этого теста сэкономит вам время и поможет подобрать вакансии специально для
            вас
          </p>

          <div class="mt-12 flex justify-center sm:mt-16">
            <RouterLink
              to="/test"
              class="inline-flex min-h-14 items-center justify-center rounded-full bg-(--button-primary) px-8 text-center text-base uppercase tracking-[0.08em] text-(--button-text) shadow-(--shadow-button) transition hover:-translate-y-0.5 hover:bg-(--button-primary-hover) sm:min-h-16 sm:min-w-100 sm:px-16 sm:text-2xl"
              style="color: var(--button-text)"
            >
              Пройти тест
            </RouterLink>
          </div>
        </div>
      </section>
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import backgroundObjectDark from '@/assets/background-object-dark.png'
import backgroundObjectLight from '@/assets/background-object-light.png'
import SiteFooter from '@/components/SiteFooter.vue'
import SiteHeader from '@/components/ThemedSiteHeader.vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const heroSectionRef = ref(null)
const isInteractive = ref(false)
const pointerOffset = ref({ x: 0, y: 0 })

let animationFrameId = 0
let mediaQueryList = null
let currentOffsetX = 0
let currentOffsetY = 0
let targetOffsetX = 0
let targetOffsetY = 0

const backgroundStyle = computed(() => ({
  '--homepage-bg-image': `url(${isDark.value ? backgroundObjectDark : backgroundObjectLight})`,
  '--homepage-bg-offset-x': `${pointerOffset.value.x}px`,
  '--homepage-bg-offset-y': `${pointerOffset.value.y}px`,
}))

function animateBackground() {
  currentOffsetX += (targetOffsetX - currentOffsetX) * 0.08
  currentOffsetY += (targetOffsetY - currentOffsetY) * 0.08

  pointerOffset.value = {
    x: Number(currentOffsetX.toFixed(2)),
    y: Number(currentOffsetY.toFixed(2)),
  }

  animationFrameId = window.requestAnimationFrame(animateBackground)
}

function updateInteractivity() {
  if (!mediaQueryList) {
    return
  }

  isInteractive.value = mediaQueryList.matches

  if (!isInteractive.value) {
    targetOffsetX = 0
    targetOffsetY = 0
    currentOffsetX = 0
    currentOffsetY = 0
    pointerOffset.value = { x: 0, y: 0 }
  }
}

function handlePointerMove(event) {
  if (!isInteractive.value || !heroSectionRef.value) {
    return
  }

  const bounds = heroSectionRef.value.getBoundingClientRect()
  const relativeX = (event.clientX - bounds.left) / bounds.width - 0.5
  const relativeY = (event.clientY - bounds.top) / bounds.height - 0.5

  targetOffsetX = -relativeX * 48
  targetOffsetY = -relativeY * 40
}

function resetPointerOffset() {
  targetOffsetX = 0
  targetOffsetY = 0
}

onMounted(() => {
  mediaQueryList = window.matchMedia('(min-width: 768px) and (pointer: fine)')
  updateInteractivity()
  mediaQueryList.addEventListener('change', updateInteractivity)
  animationFrameId = window.requestAnimationFrame(animateBackground)
})

onBeforeUnmount(() => {
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId)
  }

  mediaQueryList?.removeEventListener('change', updateInteractivity)
})
</script>

<style scoped>
.homepage-hero {
  isolation: isolate;
}

.homepage-hero__background {
  position: absolute;
  inset: 50% auto auto 50%;
  width: min(72vw, 920px);
  aspect-ratio: 1 / 1;
  background-image: var(--homepage-bg-image);
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.92;
  pointer-events: none;
  transform: translate3d(
    calc(-50% + var(--homepage-bg-offset-x, 0px)),
    calc(-50% + var(--homepage-bg-offset-y, 0px)),
    0
  );
  transition: opacity 0.3s ease;
  z-index: 0;
}

.homepage-hero__background--dark {
  opacity: 0.88;
}

@media (max-width: 767px), (pointer: coarse) {
  .homepage-hero__background {
    width: min(110vw, 640px);
    opacity: 0.82;
    transform: translate3d(-50%, -50%, 0);
  }
}
</style>

