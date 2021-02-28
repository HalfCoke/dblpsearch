<template>
  <div class="content_search">
    <el-row :gutter="10" class="">
      <el-col :span="20">
        <div class="input">
          <el-input
              placeholder="请输入内容"
              prefix-icon="el-icon-search"
              v-model="search_input"
              @change="handleSearch">
          </el-input>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="search_btn">
          <el-button
              class="button"
              type="primary"
              icon="el-icon-search"
              @click="handleSearch"
              :loading="data_loading">搜索
          </el-button>
        </div>
      </el-col>
    </el-row>
    <el-row class="el_row" :class="showRes">
      <el-col :span="24" class="papers_list">
        <div
            class="paper"
            v-for="paper in $store.state.display_papers"
            :key="genPaperKey(paper)"
            @click="handleClickLink(paper.url)"
        >
          <span v-html="paper.title" class="paper_title"></span>
          <div class="author_list">
            <span v-for="author in paper.authors" v-if="filterAuthorName(author)" class="author">{{ author }}</span>
          </div>
          <div class="other_info">
            <el-tag class="year" size="mini">{{ paper.year }}</el-tag>
            <el-tag class="abbr" size="mini">{{ paper.abbreviation }}</el-tag>
            <el-tag class="cate" :type="selectTag(paper.category)" size="mini">{{ paper.category }}</el-tag>
          </div>
        </div>
        <div v-if="showNothing()" class="noting">什么都没有啦~</div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import store from "@/store"
import { request } from "@/requests"

let timer = null
export default {
  name: "content_search",
  store,
  data () {
    return {
      search_input: '',
      data_loading: false,
      showRes: 'search_res'
    }
  },
  methods: {
    showNothing () {
      return (this.showRes.length===0&&store.state.display_papers.length===0)
    },
    genPaperKey (paper) {
      return paper.title + paper.url
    },
    filterAuthorName (author) {
      return author.indexOf("&") === -1
    },
    selectTag (category) {
      if (category === "A") return "success"
      else if (category === "B") return "warning"
      else return "info"
    },
    handleClickLink (link) {
      window.open(link)
    },
    handleSearch (val) {
      if (this.search_input === '') return
      clearTimeout(timer)
      timer = setTimeout(() => {
        let from_year = store.state.from_year
        let to_year = store.state.to_year
        let categories = store.state.categories
        let data = {
          yf: from_year,
          yt: to_year,
          category: categories,
          keys: this.search_input
        }
        this.data_loading = true

        request({
          url: "/api/v1/search",
          method: "post",
          header: {
            'Content-Type': 'application/json'
          },
          data
        }).then(res => {
          console.log(res);
          store.commit("add_papers", res.data.papers)
          store.commit("mutate_display_papers", res.data.papers)
          this.data_loading = false
          this.showRes = ""
        })
      }, 100)
    }
  }
}
</script>

<style lang="less" scoped>
.el_row {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

.search_btn {
  display: flex;

  .button {
    flex: 1;
    justify-content: center;
  }
}

.search_res {
  display: none;
}

.paper_title {
  font-weight: bold;
  color: #18181B;
  font-style: normal;
  font-size: 14px;
  display: block;
}

.papers_list {
  margin-top: 20px;
  padding-left: 10px;
  padding-right: 10px;
}

.paper {
  border-bottom: #e4e4e7 1px solid;
  padding: 8px;
  border-radius: 5px;

  &:hover {
    background-color: #fafafa;
  }
}

.author {
  color: #71717a;
  font-size: 10px;
  margin-right: 10px;
}

.author_list {
  display: block;
}

.other_info {
  color: #71717a;
  font-size: 10px;

  .abbr {
    margin-right: 5px;
    margin-left: 5px;
  }
}

.noting {
  color: #71717a;
  font-size: 10px;
}
</style>

<style>
.highlight {
  color: #409eff;
}
</style>
