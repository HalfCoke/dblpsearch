import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const date = new Date()

export default new Vuex.Store({
  state: {
    from_year: 1930,
    to_year: date.getFullYear(),
    categories: ['A', 'B', 'C'],
    search_keys: '',
    search_seq: 0,
    search_done_seq: 0
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
    // 供词云等外部入口触发检索，seq 自增保证重复点击同一关键词也能生效
    mutate_search_keys (state, keys) {
      state.search_keys = keys
      state.search_seq += 1
    },
    // 检索完成后通知词云刷新，保证搜索频次统计及时反映
    mutate_search_done (state) {
      state.search_done_seq += 1
    }
  },
  actions: {},
  modules: {}
})
