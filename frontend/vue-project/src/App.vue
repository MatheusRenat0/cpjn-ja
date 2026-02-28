<template>
  <div class="page">

    <header class="site-header">
      <div class="header-inner">
        <div class="logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <span>Consulta <strong>CNPJ</strong></span>
        </div>
        <nav class="header-nav">
          <a href="#">Início</a>
          <a href="#">Sobre</a>
        </nav>
      </div>
    </header>

    <section class="hero" :class="{ 'hero-compact': empresa || isLoading }">
      <div class="hero-inner">
        <template v-if="!empresa && !isLoading">
          <h1 class="hero-title">Consulta de CNPJ</h1>
          <p class="hero-sub">Informe o CNPJ para obter dados cadastrais completos da empresa</p>
        </template>

        <div class="search-bar">
          <div class="search-input-wrap">
            <svg class="search-ico" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              v-model="cnpjInput"
              class="search-input"
              placeholder="Digite o CNPJ"
              @keyup.enter="consultar"
              @input="formatarCNPJ"
              :disabled="isLoading"
              maxlength="18"
            />
            <button v-if="cnpjInput" class="clear-btn" @click="limpar">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <button class="btn-consultar" @click="consultar" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <template v-else>Consultar</template>
          </button>
        </div>
        