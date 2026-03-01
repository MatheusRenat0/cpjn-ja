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

        <p v-if="erro" class="search-error">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ erro }}
        </p>
      </div>
    </section>

    <div v-if="isLoading" class="result-wrap">
      <div class="skeleton-page">
        <div class="sk-company-head">
          <div class="sk sk-icon"></div>
          <div class="sk-texts">
            <div class="sk sk-h1"></div>
            <div class="sk sk-h2"></div>
          </div>
        </div>
        <div class="sk-divider"></div>
        <div v-for="n in 3" :key="n" class="sk-section">
          <div class="sk sk-stitle"></div>
          <div class="sk-rows">
            <div v-for="m in 4" :key="m" class="sk-row">
              <div class="sk sk-label"></div>
              <div class="sk sk-val"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="empresa && !isLoading" class="result-wrap">

      <div class="company-header">
        <div class="company-badge">{{ getIniciais(empresa.razao_social) }}</div>
        <div class="company-meta">
          <h2 class="co-name">{{ empresa.nome_fantasia || empresa.razao_social }}</h2>
          <p class="co-razao" v-if="empresa.nome_fantasia">{{ empresa.razao_social }}</p>
          <div class="co-pills">
            <span class="pill pill-cnpj">{{ empresa.cnpj }}</span>
            <span class="pill" :class="getStatusPill(empresa.descricao_situacao_cadastral)">
              <span class="pill-dot"></span>{{ empresa.descricao_situacao_cadastral }}
            </span>
            <span v-if="empresa.porte" class="pill pill-porte">{{ empresa.porte }}</span>
          </div>
        </div>
      </div>

      <div class="result-body">

        <div class="data-section">
          <h3 class="section-title">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h4"/></svg>
            Dados Cadastrais
          </h3>
          <div class="data-table">
            <div class="data-row"><span class="dr-label">Razão Social</span><span class="dr-val">{{ empresa.razao_social || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Nome Fantasia</span><span class="dr-val">{{ empresa.nome_fantasia || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">CNPJ</span><span class="dr-val mono">{{ empresa.cnpj }}</span></div>
            <div class="data-row"><span class="dr-label">Natureza Jurídica</span><span class="dr-val">{{ empresa.natureza_juridica || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Porte</span><span class="dr-val">{{ empresa.porte || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Capital Social</span><span class="dr-val">{{ formatarMoeda(empresa.capital_social) }}</span></div>
            <div class="data-row"><span class="dr-label">Data de Abertura</span><span class="dr-val">{{ formatarData(empresa.data_inicio_atividade) }}</span></div>
            <div class="data-row">
              <span class="dr-label">Situação</span>
              <span class="dr-val">
                <span class="inline-status" :class="getStatusPill(empresa.descricao_situacao_cadastral)">
                  <span class="pill-dot"></span>{{ empresa.descricao_situacao_cadastral }}
                </span>
              </span>
            </div>
            <div class="data-row" v-if="empresa.data_situacao_cadastral"><span class="dr-label">Data da Situação</span><span class="dr-val">{{ formatarData(empresa.data_situacao_cadastral) }}</span></div>
            <div class="data-row" v-if="empresa.motivo_situacao_cadastral"><span class="dr-label">Motivo</span><span class="dr-val">{{ empresa.motivo_situacao_cadastral }}</span></div>
          </div>
        </div>

        <div class="two-col">
          <div class="data-section">
            <h3 class="section-title">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              Endereço
            </h3>
            <div class="data-table">
              <div class="data-row"><span class="dr-label">Logradouro</span><span class="dr-val">{{ empresa.logradouro || '—' }}, {{ empresa.numero || 'S/N' }}</span></div>
              <div class="data-row" v-if="empresa.complemento"><span class="dr-label">Complemento</span><span class="dr-val">{{ empresa.complemento }}</span></div>
              <div class="data-row"><span class="dr-label">Bairro</span><span class="dr-val">{{ empresa.bairro || '—' }}</span></div>
              <div class="data-row"><span class="dr-label">Município / UF</span><span class="dr-val">{{ empresa.municipio || '—' }} / {{ empresa.uf || '—' }}</span></div>
              <div class="data-row"><span class="dr-label">CEP</span><span class="dr-val mono">{{ empresa.cep || '—' }}</span></div>
            </div>
          </div>

          <div class="data-section">
            <h3 class="section-title">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.77 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.18z"/></svg>
              Contato
            </h3>
            <div class="data-table">
              <div class="data-row"><span class="dr-label">Telefone 1</span><span class="dr-val mono">{{ formatTel(empresa.ddd_telefone_1, empresa.telefone_1) }}</span></div>
              <div class="data-row" v-if="empresa.ddd_telefone_2"><span class="dr-label">Telefone 2</span><span class="dr-val mono">{{ formatTel(empresa.ddd_telefone_2, empresa.telefone_2) }}</span></div>
              <div class="data-row"><span class="dr-label">E-mail</span><span class="dr-val">{{ empresa.email || '—' }}</span></div>
            </div>
            
            <template v-if="empresa.qsa && empresa.qsa.length">
              <h3 class="section-title" style="margin-top:1px">
                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                Quadro Societário
              </h3>
              <div class="socio-list">
                <div v-for="s in empresa.qsa" :key="s.nome_socio" class="socio-item">
                  <div class="socio-avatar">{{ s.nome_socio?.[0] }}</div>
                  <div class="socio-info">
                    <p class="socio-name">{{ s.nome_socio }}</p>
                    <p class="socio-qual">{{ s.qualificacao_socio }}</p>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
        
        <div class="data-section" v-if="empresa.cnae_fiscal">
          <h3 class="section-title">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            Atividade Econômica (CNAE)
          </h3>
          <div class="cnae-block primary-cnae">
            <span class="cnae-badge">PRINCIPAL</span>
            <div class="cnae-info">
              <code class="cnae-code">{{ empresa.cnae_fiscal }}</code>
              <span class="cnae-desc">{{ empresa.cnae_fiscal_descricao || '—' }}</span>
            </div>
          </div>
          <template v-if="empresa.cnaes_secundarios && empresa.cnaes_secundarios.length">
            <p class="secondary-label">Secundárias ({{ empresa.cnaes_secundarios.length }})</p>
            <div v-for="cnae in empresa.cnaes_secundarios" :key="cnae.codigo" class="cnae-block secondary-cnae">
              <div class="cnae-info">
                <code class="cnae-code">{{ cnae.codigo }}</code>
                <span class="cnae-desc">{{ cnae.descricao }}</span>
              </div>
            </div>
          </template>
        </div>

      </div>

      <div class="result-footer">
        <span>Dados obtidos via Receita Federal do Brasil</span>
        <button class="btn-export" @click="exportar">
          <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Exportar JSON
        </button>
      </div>
    </div>

    <footer class="site-footer">
      <p>Consulta CNPJ — Dados da Receita Federal do Brasil</p>
    </footer>

  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ConsultaCNPJ',
  data() {
    return {
      cnpjInput: '',
      empresa: null,
      isLoading: false,
      erro: null,
    };
  },
  methods: {
    async consultar() {
      const limpo = this.cnpjInput.replace(/\D/g, '');
      if (!limpo) { this.erro = 'Informe um CNPJ válido.'; return; }
      if (limpo.length !== 14) { this.erro = 'O CNPJ deve ter 14 dígitos.'; return; }
      this.isLoading = true;
      this.erro = null;
      this.empresa = null;
      try {
        const { data } = await api.get(`/cnpj/${limpo}`);
        this.empresa = data;
      } catch (err) {
        this.erro = err.response?.data?.erro || 'Erro ao conectar com o servidor.';
      } finally {
        this.isLoading = false;
      }
    },

    formatarCNPJ(e) {
      let v = e.target.value.replace(/\D/g, '');
      v = v.replace(/^(\d{2})(\d)/, '$1.$2');
      v = v.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
      v = v.replace(/\.(\d{3})(\d)/, '.$1/$2');
      v = v.replace(/(\d{4})(\d)/, '$1-$2');
      this.cnpjInput = v;
      this.erro = null;
    },

    limpar() { this.cnpjInput = ''; this.empresa = null; this.erro = null; },

    getIniciais(n) {
      if (!n) return 'EM';
      return n.trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase();
    },

    getStatusPill(s) {
      if (!s) return '';
      const l = s.toLowerCase();
      if (l.includes('ativa')) return 'pill-ativa';
      if (l.includes('suspend') || l.includes('inapta')) return 'pill-suspensa';
      if (l.includes('baixada') || l.includes('cancelada')) return 'pill-baixada';
      return 'pill-outro';
    },

    formatarData(d) {
      if (!d) return '—';
      try {
        const iso = d.includes('-') ? d : `${d.slice(0,4)}-${d.slice(4,6)}-${d.slice(6,8)}`;
        return new Date(iso + 'T00:00:00').toLocaleDateString('pt-BR');
      } catch { return d; }
    },

    formatarMoeda(v) {
      if (!v) return '—';
      return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    },

    formatTel(ddd, tel) {
      if (!ddd && !tel) return '—';
      return `(${ddd || ''}) ${tel || ''}`.trim();
    },

    exportar() {
      const blob = new Blob([JSON.stringify(this.empresa, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `cnpj_${this.empresa.cnpj?.replace(/\D/g,'')}.json`;
      a.click();
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body {
  margin: 0;
  padding: 0;
  background: #f7f8fa;
  font-family: 'Inter', sans-serif;
}
</style>

<style scoped>
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page {
  min-height: 100vh;
  width: 100%;
  background: #f7f8fa;
  font-family: 'Inter', sans-serif;
  color: #1c1f26;
  font-size: 14px;
  line-height: 1.5;
}

/* ===== HEADER ===== */
.site-header {
  background: #fff;
  border-bottom: 1px solid #e8eaee;
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
}

.header-inner {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: #1c1f26;
  font-weight: 400;
}

.logo strong {
  font-weight: 700;
}

.logo svg {
  color: #2563eb;
}

.header-nav {
  display: flex;
  gap: 24px;
}

.header-nav a {
  font-size: 13px;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s;
}

.header-nav a:hover {
  color: #1c1f26;
}

/* ===== HERO ===== */
.hero {
  background: #fff;
  border-bottom: 1px solid #e8eaee;
  padding: 72px 24px 56px;
  text-align: center;
  transition: padding 0.3s ease;
  width: 100%;
}

.hero.hero-compact {
  padding: 28px 24px;
}

.hero-inner {
  max-width: 620px;
  margin: 0 auto;
}

.hero-title {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #111318;
  margin-bottom: 10px;
}

.hero-sub {
  font-size: 15px;
  color: #6b7280;
  margin-bottom: 32px;
}

/* ===== SEARCH BAR ===== */
.search-bar {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.search-input-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f3f4f6;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 0 14px;
  gap: 10px;
  transition: all 0.15s;
  min-width: 0;
}

.search-input-wrap:focus-within {
  background: #fff;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.10);
}

.search-ico {
  color: #9ca3af;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 15px;
  font-family: 'JetBrains Mono', monospace;
  color: #1c1f26;
  letter-spacing: 0.5px;
  padding: 11px 0;
  min-width: 0;
}

.search-input::placeholder {
  font-family: 'Inter', sans-serif;
  color: #9ca3af;
  font-size: 14px;
  letter-spacing: 0;
}

.search-input:disabled {
  cursor: not-allowed;
}

.clear-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
  padding: 2px;
  border-radius: 4px;
  flex-shrink: 0;
}

.clear-btn:hover {
  color: #4b5563;
}

.btn-consultar {
  height: 44px;
  padding: 0 24px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.15s;
  flex-shrink: 0;
}

.btn-consultar:hover:not(:disabled) {
  background: #1d4ed8;
}

.btn-consultar:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.search-error {
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
  margin-top: 14px;
  font-size: 13px;
  color: #dc2626;
  font-weight: 500;
}

/* ===== SPINNER ===== */
.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ===== RESULT WRAP ===== */
.result-wrap {
  width: 100%;
  max-width: 1200px;
  margin: 32px auto;
  padding: 0 32px;
}

/* ===== SKELETON ===== */
.skeleton-page {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #e8eaee;
  overflow: hidden;
}

.sk-company-head {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 28px 28px 24px;
}

.sk {
  background: linear-gradient(90deg, #f0f2f5 25%, #e5e7eb 50%, #f0f2f5 75%);
  background-size: 200% 100%;
  animation: shimmer 1.3s infinite;
  border-radius: 6px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.sk-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  flex-shrink: 0;
}

.sk-texts {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.sk-h1 {
  height: 22px;
  width: 280px;
  max-width: 100%;
}

.sk-h2 {
  height: 14px;
  width: 180px;
  max-width: 100%;
}

.sk-divider {
  height: 1px;
  background: #e8eaee;
}

.sk-section {
  padding: 24px 28px;
  border-bottom: 1px solid #f3f4f6;
}

.sk-stitle {
  height: 13px;
  width: 130px;
  margin-bottom: 16px;
}

.sk-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sk-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.sk-label {
  height: 12px;
  width: 120px;
}

.sk-val {
  height: 12px;
  width: 200px;
  max-width: 50%;
}

/* ===== COMPANY HEADER ===== */
.company-header {
  background: #fff;
  border: 1px solid #e8eaee;
  border-radius: 14px;
  padding: 24px 28px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 12px;
}

.company-badge {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1.5px solid #dbeafe;
}

.company-meta {
  flex: 1;
  min-width: 0;
}

.co-name {
  font-size: clamp(16px, 2.5vw, 22px);
  font-weight: 700;
  color: #111318;
  line-height: 1.25;
  margin-bottom: 4px;
}

.co-razao {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 12px;
}

.co-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 6px;
}

.pill-cnpj {
  background: #f3f4f6;
  color: #374151;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px;
}

.pill-porte {
  background: #f0f9ff;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.pill-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.pill-ativa {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.pill-suspensa {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}

.pill-baixada {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.pill-outro {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
}

/* ===== RESULT BODY ===== */
.result-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ===== DATA SECTION ===== */
.data-section {
  background: #fff;
  border: 1px solid #e8eaee;
  border-radius: 14px;
  overflow: hidden;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #6b7280;
  padding: 14px 24px 12px;
  border-bottom: 1px solid #f3f4f6;
}

.section-title svg {
  color: #9ca3af;
}

/* ===== DATA TABLE ===== */
.data-table {
  padding: 4px 0 6px;
}

.data-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 24px;
  padding: 9px 24px;
  border-bottom: 1px solid #f9fafb;
  transition: background 0.1s;
}

.data-row:last-child {
  border-bottom: none;
}

.data-row:hover {
  background: #fafbfc;
}

.dr-label {
  font-size: 13px;
  color: #6b7280;
  white-space: nowrap;
  flex-shrink: 0;
}

.dr-val {
  font-size: 13.5px;
  font-weight: 500;
  color: #111318;
  text-align: right;
  word-break: break-word;
}

.dr-val.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

.inline-status {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 9px;
  border-radius: 5px;
}

/* ===== TWO COL ===== */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

@media (max-width: 700px) {
  .two-col {
    grid-template-columns: 1fr;
  }
}

/* ===== CNAE ===== */
.cnae-block {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.cnae-block:last-child {
  border-bottom: none;
}

.primary-cnae {
  background: #fafeff;
}

.secondary-cnae {
  background: #fafafa;
}

.cnae-badge {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.8px;
  padding: 3px 8px;
  border-radius: 5px;
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #dbeafe;
  white-space: nowrap;
  margin-top: 3px;
  flex-shrink: 0;
}

.cnae-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cnae-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px;
  font-weight: 600;
  color: #374151;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 4px;
  white-space: nowrap;
}

.cnae-desc {
  font-size: 13px;
  color: #374151;
}

.secondary-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: #9ca3af;
  padding: 10px 24px 4px;
}

/* ===== SÓCIOS ===== */
.socio-list {
  padding: 4px 0;
}

.socio-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 24px;
  border-bottom: 1px solid #f9fafb;
}

.socio-item:last-child {
  border-bottom: none;
}

.socio-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f3f4f6;
  color: #374151;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.socio-name {
  font-size: 13px;
  font-weight: 600;
  color: #111318;
}

.socio-qual {
  font-size: 12px;
  color: #6b7280;
}

/* ===== RESULT FOOTER ===== */
.result-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 4px;
  font-size: 12px;
  color: #9ca3af;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 1.5px solid #e5e7eb;
  color: #374151;
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 12.5px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-export:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

/* ===== SITE FOOTER ===== */
.site-footer {
  text-align: center;
  padding: 28px 24px;
  font-size: 12px;
  color: #9ca3af;
  border-top: 1px solid #e8eaee;
  margin-top: 16px;
  background: #fff;
  width: 100%;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 600px) {
  .header-inner {
    padding: 0 16px;
  }

  .result-wrap {
    padding: 0 16px;
    margin: 20px auto;
  }

  .company-header {
    padding: 16px;
    gap: 14px;
  }

  .company-badge {
    width: 42px;
    height: 42px;
    font-size: 15px;
  }

  .data-row {
    gap: 12px;
    padding: 9px 16px;
  }

  .dr-label {
    font-size: 12px;
  }

  .dr-val {
    font-size: 12.5px;
  }

  .section-title {
    padding: 12px 16px 10px;
  }

  .cnae-block {
    padding: 10px 16px;
  }

  .socio-item {
    padding: 10px 16px;
  }

  .hero {
    padding: 40px 16px 32px;
  }

  .hero.hero-compact {
    padding: 20px 16px;
  }

  .btn-consultar {
    padding: 0 16px;
    font-size: 13px;
  }
}
</style>