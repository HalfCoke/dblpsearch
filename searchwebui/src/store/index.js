import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const date = new Date()

export default new Vuex.Store({
  state: {
    from_year: 1930,
    to_year: date.getFullYear(),
    categories: ['A', 'B', 'C']
  },
  mutations: {
    mutate_from_year (state, n) {
      state.from_year = n
    },
    mutate_to_year (state, n) {
      state.to_year = n
    },
    mutate_categories (state, val) {
      state.categories = val
    }
  },
  actions: {},
  modules: {}
})
