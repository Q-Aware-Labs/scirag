import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export interface Paper {
  paper_id: string;
  title: string;
  authors: string[];
  published: string;
  url: string;
  pdf_url: string;
  summary: string;
  categories: string[];
}

export interface SearchResponse {
  success: boolean;
  papers: Paper[];
  count: number;
  message?: string;
}

export interface ProcessResponse {
  success: boolean;
  total: number;
  processed: number;
  failed: number;
  message: string;
}

export interface Source {
  title: string;
  authors: string[];
  published: string;
  url: string;
}

export interface APIConfig {
  provider: 'claude' | 'openai' | 'deepseek' | 'gemini';
  apiKey: string;
  model?: string;
}

export interface GuardrailWarning {
  type: string;
  message: string;
  severity: 'warning' | 'error';
}

export interface QueryResponse {
  success: boolean;
  answer: string;
  sources: Source[];
  message?: string;
  guardrail_warning?: GuardrailWarning;
}

export const api = {
  searchPapers: async (query: string, maxResults: number = 3): Promise<SearchResponse> => {
    const response = await axios.post(`${API_BASE_URL}/search`, {
      query,
      max_results: maxResults
    });
    return response.data;
  },

  processPapers: async (paperIds: string[], apiConfig?: APIConfig | null): Promise<ProcessResponse> => {
    const requestData: {
      paper_ids: string[];
      api_config?: {
        provider: string;
        api_key: string;
        model?: string;
      };
    } = {
      paper_ids: paperIds
    };

    // Include API config if provided
    if (apiConfig) {
      requestData.api_config = {
        provider: apiConfig.provider,
        api_key: apiConfig.apiKey,
        model: apiConfig.model
      };
    }

    const response = await axios.post(`${API_BASE_URL}/papers/process`, requestData);
    return response.data;
  },

  query: async (
    question: string,
    nResults: number = 5,
    apiConfig?: APIConfig | null
  ): Promise<QueryResponse> => {
    const requestData: {
      question: string;
      n_results: number;
      api_config?: {
        provider: string;
        api_key: string;
        model?: string;
      };
    } = {
      question,
      n_results: nResults
    };

    // Include API config if provided
    if (apiConfig) {
      requestData.api_config = {
        provider: apiConfig.provider,
        api_key: apiConfig.apiKey,
        model: apiConfig.model
      };
    }

    const response = await axios.post(`${API_BASE_URL}/query`, requestData);
    return response.data;
  },

  listPapers: async (): Promise<Paper[]> => {
    const response = await axios.get(`${API_BASE_URL}/papers`);
    return response.data.papers;
  }
};