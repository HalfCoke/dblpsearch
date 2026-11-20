import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const date = new Date()

export default new Vuex.Store({
  state: {
    from_year: 1930,
    to_year: date.getFullYear(),
    categories: ['A', 'B', 'C'],
    papers: null,
    display_papers: []
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
    },
    add_papers (state, papers) {
      state.papers = papers
    },
    mutate_display_papers (state, papers) {
      state.display_papers = papers
    },
    mutate_display_papers_by_filter (state) {
      if (!state.papers) {
        state.display_papers = []
        return
      }
      state.display_papers = state.papers.filter(paper => (
        state.categories.indexOf(paper.category) !== -1 &&
        paper.year >= state.from_year &&
        paper.year <= state.to_year
      ))
    }
  },
  actions: {},
  modules: {}
})
