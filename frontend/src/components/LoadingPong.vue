<template>
  <div
    ref="fieldRef"
    class="loading-pong"
    :class="{ 'loading-pong--compact': compact }"
  >
    <div
      class="loading-pong__arena"
      @pointermove="handlePointerMove"
      @pointerdown="handlePointerMove"
      @pointerenter="handlePointerMove"
      @touchstart.prevent="handleTouchMove"
      @touchmove.prevent="handleTouchMove"
    >
      <div class="loading-pong__center-line" aria-hidden="true" />
      <div
        class="loading-pong__paddle loading-pong__paddle--left"
        :style="{ transform: `translateY(${leftPaddleY}px)` }"
        aria-hidden="true"
      />
      <div
        class="loading-pong__paddle loading-pong__paddle--right"
        :style="{ transform: `translateY(${rightPaddleY}px)` }"
        aria-hidden="true"
      />
      <div
        class="loading-pong__ball"
        :class="{ 'loading-pong__ball--reset': isResetting }"
        :style="{ transform: `translate(${ballX}px, ${ballY}px)` }"
        aria-hidden="true"
      />
      <div class="loading-pong__glow loading-pong__glow--left" aria-hidden="true" />
      <div class="loading-pong__glow loading-pong__glow--right" aria-hidden="true" />
    </div>

    <p class="loading-pong__title">
      {{ title }}
    </p>
    <p v-if="subtitle" class="loading-pong__subtitle">
      {{ subtitle }}
    </p>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Формируем персональный результат',
  },
  subtitle: {
    type: String,
    default: '',
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

const fieldRef = ref(null)
const leftPaddleY = ref(70)
const rightPaddleY = ref(70)
const ballX = ref(150)
const ballY = ref(90)
const isResetting = ref(false)

let animationFrameId = 0
let lastTimestamp = 0
let resetTimeoutId = 0
let lastInteractionAt = 0

const pressedKeys = {
  up: false,
  down: false,
}

const state = {
  width: 320,
  height: 200,
  paddleWidth: 10,
  paddleHeight: 52,
  ballSize: 12,
  leftY: 70,
  rightY: 70,
  ballPosX: 150,
  ballPosY: 90,
  velocityX: 180,
  velocityY: 120,
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max)
}

function syncBounds() {
  const rect = fieldRef.value?.querySelector('.loading-pong__arena')?.getBoundingClientRect()

  if (!rect) {
    return
  }

  state.width = rect.width
  state.height = rect.height
  resetRound(Math.sign(state.velocityX) || 1)
}

function applyState() {
  leftPaddleY.value = state.leftY
  rightPaddleY.value = state.rightY
  ballX.value = state.ballPosX
  ballY.value = state.ballPosY
}

function setLeftPaddleFromClientY(clientY) {
  const rect = fieldRef.value?.querySelector('.loading-pong__arena')?.getBoundingClientRect()

  if (!rect) {
    return
  }

  const relativeY = clientY - rect.top - state.paddleHeight / 2
  state.leftY = clamp(relativeY, 0, state.height - state.paddleHeight)
  lastInteractionAt = performance.now()
  applyState()
}

function resetRound(direction = 1) {
  state.leftY = (state.height - state.paddleHeight) / 2
  state.rightY = (state.height - state.paddleHeight) / 2
  state.ballPosX = (state.width - state.ballSize) / 2
  state.ballPosY = (state.height - state.ballSize) / 2
  state.velocityX = 180 * direction
  state.velocityY = (Math.random() > 0.5 ? 1 : -1) * (110 + Math.random() * 35)
  applyState()
}

function scheduleReset(nextDirection) {
  isResetting.value = true
  window.clearTimeout(resetTimeoutId)
  resetTimeoutId = window.setTimeout(() => {
    resetRound(nextDirection)
    isResetting.value = false
  }, 480)
}

function updatePaddles(deltaSeconds) {
  const ballCenter = state.ballPosY + state.ballSize / 2

  const rightTarget = ballCenter - state.paddleHeight / 2 + Math.cos(state.ballPosY * 0.02) * 6
  const keyboardSpeed = 320 * deltaSeconds
  const rightFollow = 1 - Math.exp(-7.2 * deltaSeconds)
  const hasKeyboardInput = pressedKeys.up || pressedKeys.down

  if (hasKeyboardInput) {
    if (pressedKeys.up) {
      state.leftY -= keyboardSpeed
    }

    if (pressedKeys.down) {
      state.leftY += keyboardSpeed
    }
  }

  state.rightY += (rightTarget - state.rightY) * rightFollow

  state.leftY = clamp(state.leftY, 0, state.height - state.paddleHeight)
  state.rightY = clamp(state.rightY, 0, state.height - state.paddleHeight)
}

function bounceFromPaddle(paddleY, isRightPaddle) {
  const relativeHit = (state.ballPosY + state.ballSize / 2 - (paddleY + state.paddleHeight / 2)) / (state.paddleHeight / 2)
  state.velocityY = relativeHit * 185
  state.velocityX *= -1

  if (isRightPaddle) {
    state.ballPosX = state.width - state.paddleWidth - state.ballSize - 18
  } else {
    state.ballPosX = 18 + state.paddleWidth
  }
}

function tick(timestamp) {
  if (!lastTimestamp) {
    lastTimestamp = timestamp
  }

  const deltaSeconds = Math.min((timestamp - lastTimestamp) / 1000, 0.032)
  lastTimestamp = timestamp

  if (!isResetting.value) {
    updatePaddles(deltaSeconds)

    state.ballPosX += state.velocityX * deltaSeconds
    state.ballPosY += state.velocityY * deltaSeconds

    if (state.ballPosY <= 0 || state.ballPosY >= state.height - state.ballSize) {
      state.ballPosY = clamp(state.ballPosY, 0, state.height - state.ballSize)
      state.velocityY *= -1
    }

    const leftCollisionX = 18 + state.paddleWidth
    const rightCollisionX = state.width - 18 - state.paddleWidth - state.ballSize
    const intersectsLeftPaddle =
      state.ballPosX <= leftCollisionX &&
      state.ballPosY + state.ballSize >= state.leftY &&
      state.ballPosY <= state.leftY + state.paddleHeight
    const intersectsRightPaddle =
      state.ballPosX >= rightCollisionX &&
      state.ballPosY + state.ballSize >= state.rightY &&
      state.ballPosY <= state.rightY + state.paddleHeight

    if (intersectsLeftPaddle && state.velocityX < 0) {
      bounceFromPaddle(state.leftY, false)
    }

    if (intersectsRightPaddle && state.velocityX > 0) {
      bounceFromPaddle(state.rightY, true)
    }

    if (state.ballPosX < -state.ballSize) {
      scheduleReset(1)
    } else if (state.ballPosX > state.width + state.ballSize) {
      scheduleReset(-1)
    }

    applyState()
  }

  animationFrameId = window.requestAnimationFrame(tick)
}

function handleResize() {
  syncBounds()
}

function handlePointerMove(event) {
  setLeftPaddleFromClientY(event.clientY)
}

function handleTouchMove(event) {
  const touch = event.touches?.[0]

  if (!touch) {
    return
  }

  setLeftPaddleFromClientY(touch.clientY)
}

function handleKeyDown(event) {
  const key = event.key.toLowerCase()

  if (key === 'w' || key === 'ц') {
    pressedKeys.up = true
    lastInteractionAt = performance.now()
  }

  if (key === 's' || key === 'ы') {
    pressedKeys.down = true
    lastInteractionAt = performance.now()
  }
}

function handleKeyUp(event) {
  const key = event.key.toLowerCase()

  if (key === 'w' || key === 'ц') {
    pressedKeys.up = false
  }

  if (key === 's' || key === 'ы') {
    pressedKeys.down = false
  }
}

onMounted(() => {
  syncBounds()
  window.addEventListener('resize', handleResize)
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  animationFrameId = window.requestAnimationFrame(tick)
})

onBeforeUnmount(() => {
  window.cancelAnimationFrame(animationFrameId)
  window.clearTimeout(resetTimeoutId)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
})
</script>

<style scoped>
.loading-pong {
  width: min(100%, 30rem);
  margin: 0 auto;
}

.loading-pong--compact {
  width: min(100%, 22rem);
}

.loading-pong__arena {
  position: relative;
  overflow: hidden;
  width: 100%;
  aspect-ratio: 16 / 10;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 1.8rem;
  background:
    radial-gradient(circle at 20% 50%, rgba(93, 114, 255, 0.18), transparent 38%),
    radial-gradient(circle at 80% 50%, rgba(255, 52, 95, 0.14), transparent 34%),
    linear-gradient(180deg, rgba(237, 183, 255, 0.12), rgba(237, 183, 255, 0.04));
  box-shadow: 0 24px 64px rgba(9, 5, 40, 0.18);
  backdrop-filter: blur(18px);
}

.loading-pong__center-line {
  position: absolute;
  top: 10%;
  bottom: 10%;
  left: 50%;
  width: 2px;
  transform: translateX(-50%);
  background: repeating-linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.22) 0 12px,
    transparent 12px 24px
  );
}

.loading-pong__paddle,
.loading-pong__ball {
  position: absolute;
  will-change: transform;
}

.loading-pong__paddle {
  top: 0;
  width: 10px;
  height: 52px;
  border-radius: 9999px;
  background: linear-gradient(180deg, #f7d0ff 0%, #ffffff 100%);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12);
}

.loading-pong__paddle--left {
  left: 18px;
}

.loading-pong__paddle--right {
  right: 18px;
}

.loading-pong__ball {
  top: 0;
  width: 12px;
  height: 12px;
  border-radius: 9999px;
  background: #ff7ea5;
  box-shadow: 0 0 22px rgba(255, 126, 165, 0.55);
  transition: opacity 0.28s ease, transform 0.1s linear;
}

.loading-pong__ball--reset {
  opacity: 0.3;
}

.loading-pong__glow {
  position: absolute;
  top: 50%;
  width: 5rem;
  height: 5rem;
  border-radius: 9999px;
  filter: blur(24px);
  opacity: 0.42;
  transform: translateY(-50%);
}

.loading-pong__glow--left {
  left: -1rem;
  background: rgba(93, 114, 255, 0.34);
}

.loading-pong__glow--right {
  right: -1rem;
  background: rgba(255, 52, 95, 0.25);
}

.loading-pong__title {
  margin: 1rem 0 0;
  color: rgba(255, 255, 255, 0.88);
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.22em;
  line-height: 1.2;
  text-align: center;
  text-transform: uppercase;
}

.loading-pong__subtitle {
  margin: 0.65rem 0 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.92rem;
  line-height: 1.45;
  text-align: center;
}

@media (max-width: 767px) {
  .loading-pong {
    width: min(100%, 25rem);
  }

  .loading-pong__arena {
    border-radius: 1.35rem;
  }

  .loading-pong__title {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
  }

  .loading-pong__subtitle {
    font-size: 0.82rem;
  }
}
</style>
