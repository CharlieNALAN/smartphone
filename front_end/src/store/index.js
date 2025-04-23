// store.js  
import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    scenicOptions: [],
    allAttractions: [],
    attractionData: [],
    currentPage: 1,
    perPage: 10,
  },
  mutations: {
    SET_SCENIC_OPTIONS(state, scenicOptions) {
      state.scenicOptions = scenicOptions;
    },
    SET_ATTRACTION_DATA(state, data) {
      state.attractionData = data;
    },
    SET_CURRENT_PAGE(state, page) {
      state.currentPage = page;
    },
    SET_ALL_ATTRACTIONS(state, allAttractions) {
      state.allAttractions = allAttractions;
    }
  },
  actions: {
    fetchScenicOptions({ commit }) {
      axios.get('http://localhost:8000/api/scenic/')
        .then(response => {
          commit('SET_SCENIC_OPTIONS', response.data);
        })
        .catch(error => {
          console.error('Error fetching scenic options:', error);
        });
    },
    // async fetchAttractionData({ commit, state }) {
    //   try {
    //     const response = await axios.get(`http://localhost:8000/attraction/?page=${state.currentPage}`);
    //     commit('SET_ATTRACTION_DATA', response.data.results);
    //   } catch (error) {
    //     console.error('Error fetching attractions:', error);
    //   }
    // },
    fetchAllAttractions({ commit }) {
      axios.get('http://localhost:8000/api/attractions/')
        .then(response => {
          commit('SET_ALL_ATTRACTIONS', response.data);
        })
        .catch(error => {
          console.error('Error fetching all attractions:', error);
        });
    }
  }
});