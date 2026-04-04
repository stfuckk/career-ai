<template>
  <footer class="relative z-20 px-4 sm:px-8 lg:px-12">
    <div class="authlike-footer mx-auto flex w-full max-w-6xl flex-col gap-3 px-5 py-3 sm:flex-row sm:items-center sm:justify-between sm:px-8">
      <span>Войтивайти</span>
      <a
        href="https://t.me/whya1ive7"
        target="_blank"
        rel="noreferrer"
        class="authlike-footer__link"
      >
        Написать нам в telegram
      </a>
    </div>
  </footer>
</template>

<style scoped>
.authlike-footer {
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1rem 1rem 0 0;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.12), rgba(124, 120, 255, 0.14));
  color: rgba(255, 255, 255, 0.52);
  font-size: 0.85rem;
  letter-spacing: 0.01em;
  backdrop-filter: blur(16px);
}

.authlike-footer__link {
  transition: opacity 0.2s ease;
}

.authlike-footer__link:hover {
  opacity: 0.78;
}

@media (max-width: 767px) {
  .authlike-footer {
    text-align: left;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
