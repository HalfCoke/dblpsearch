import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
let date = new Date;
export default new Vuex.Store({
  state: {
    from_year: 1930,
    to_year: date.getFullYear(),
    categories: ['A', 'B', 'C'],
    papers: null,
    display_papers: null
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
      let pre_display_papers = []
      for (let paper of state.papers) {
        if ((state.categories.indexOf(paper.category) !== -1) && (paper.year >= state.from_year && paper.year <= state.to_year)){
          pre_display_papers.push(paper)
        }
      }
      this.commit('mutate_display_papers', pre_display_papers)
    }
  },
  actions: {},
  modules: {}
})
