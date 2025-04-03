<template>
  <div class="search-container">
    <h1>Busca de Operadoras de Saúde</h1>
    <div class="search-box">
      <input 
        v-model="query" 
        @input="debouncedFetch" 
        placeholder="Digite para buscar por nome, registro ANS, CNPJ, modalidade ou localização" 
        class="search-input"
      />
      <div class="search-icon" v-if="!isLoading">🔍</div>
      <div class="loading-icon" v-else>⌛</div>
    </div>
    
    <div v-if="!operadoras.length && !isLoading && query" class="no-results">
      Nenhuma operadora encontrada para "{{ query }}".
    </div>
    
    <div v-if="operadoras.length" class="results-count">
      {{ operadoras.length }} operadora(s) encontrada(s)
    </div>
    
    <div class="results-container">
      <div 
        v-for="operadora in operadoras" 
        :key="operadora.id"
        class="result-card"
      >
        <div class="card-header">
          <h3>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</h3>
          <span class="registro-ans">Registro ANS: {{ operadora.Registro_ANS }}</span>
        </div>
        <div class="card-body">
          <p><strong>Razão Social:</strong> {{ operadora.Razao_Social }}</p>
          <p><strong>CNPJ:</strong> {{ operadora.CNPJ }}</p>
          <p><strong>Modalidade:</strong> {{ operadora.Modalidade }}</p>
          <p><strong>Localização:</strong> {{ operadora.Cidade }}/{{ operadora.UF }}</p>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      operadoras: [],
      isLoading: false,
      timeout: null
    };
  },
  methods: {
    debouncedFetch() {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        this.fetchOperadoras();
      }, 300);
    },
    async fetchOperadoras() {
      if (!this.query) {
        this.operadoras = [];
        return;
      }
      
      this.isLoading = true;
      
      try {
        const response = await axios.get(`http://localhost:5000/search`, {
          params: { query: this.query }
        });
        this.operadoras = response.data.results;
      } catch (error) {
        console.error("Erro ao buscar operadoras:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

