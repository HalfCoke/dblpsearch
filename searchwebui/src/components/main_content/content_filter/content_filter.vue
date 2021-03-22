<template>
  <div class="content_filter">
    <div class="text">
      <p>过滤器</p>
    </div>
    <div class="category">
      <div class="text">
        <p>会议/期刊类别</p>
      </div>
      <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
      <div style="margin: 15px 0;"></div>
      <el-checkbox-group v-model="checkedCategories" @change="handleCheckedCategoriesChange">
        <el-checkbox v-for="category in categories" :label="category" :key="category">{{ category }}</el-checkbox>
      </el-checkbox-group>
    </div>
    <div class="content_time">
      <div class="text">
        <p>时间范围</p>
      </div>
      <div class="slider">
        <el-slider
            v-model="value"
            range
            :marks="marks"
            :max="max"
            :min="min"
            @change="handleSliderChange"
            @input="handleSlider">
        </el-slider>
      </div>
      <div class="input_wrapper">
        <div class="time_input">
          <el-input
              @input="handleFromYear"
              v-model="from_year"
              placeholder="起始年份"

          ></el-input>
        </div>
        <div class="time_input">
          <el-input
              @input="handleToYear"
              v-model="to_year"
              placeholder="终止年份"

          ></el-input>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/store"

const categoryOptions = ['A', 'B', 'C'];
let slider_timer = null
let input_timer = null
let check_timer = null
export default {
  name: "content_filter",
  store,
  data () {
    return {
      checkAll: true,
      checkedCategories: ['A', 'B', 'C'],
      categories: categoryOptions,
      isIndeterminate: false,
      value: [2015, 2021],
      min: 1930,
      max: 2021,
      marks: {},
      from_year: '',
      to_year: ''
    };
  },
  created () {
    let date = new Date;
    this.max = date.getFullYear();
    this.value[1] = this.max;
    this.marks = {
      1930: '1930',
      1980: '1980',
      2000: '2000',
      [this.max]: this.max.toString()
    }
  },
  methods: {
    handleCheckAllChange (val) {
      this.checkedCategories = val ? categoryOptions : [];
      this.isIndeterminate = false;
      clearTimeout(check_timer)
      check_timer = setTimeout(()=>{
        store.commit('mutate_categories', this.checkedCategories)
        store.commit('mutate_display_papers_by_filter')
      },300)
    },
    handleCheckedCategoriesChange (value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.categories.length;
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.categories.length;
      clearTimeout(check_timer)
      check_timer = setTimeout(()=>{
        store.commit('mutate_categories', this.checkedCategories)
        store.commit('mutate_display_papers_by_filter')
      },300)
    },
    handleSlider (val) {
      this.from_year = this.value[0]
      this.to_year = this.value[1]
      clearTimeout(slider_timer)
      slider_timer = setTimeout(() => {
        store.commit('mutate_from_year', this.from_year)
        store.commit('mutate_to_year', this.to_year)
        if (store.state.papers !== null) {
          store.commit('mutate_display_papers_by_filter')
        }
      }, 300)
    },
    handleSliderChange (val) {

    },
    handleFromYear (val) {
      let from = this.value[0]
      let to = this.value[1]
      if (1930 <= val) {
        if (val <= to) {
          from = val
        } else {
          from = to
        }
        this.value = [from, to]
        clearTimeout(input_timer)
        input_timer = setTimeout(() => {
          if (store.state.papers !== null) {
            store.commit('mutate_from_year', from)
            store.commit('mutate_display_papers_by_filter')
          }
        }, 300)
      }
    },
    handleToYear (val) {
      let from = this.value[0]
      let to = this.value[1]
      if (from <= val && val <= this.max) {
        to = val
        this.value = [from, to]
        clearTimeout(input_timer)
        input_timer = setTimeout(() => {
          if (store.state.papers !== null) {
            store.commit('mutate_to_year', to)
            store.commit('mutate_display_papers_by_filter')
          }
        }, 300)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.text {
  font-style: normal;
  font-weight: bold;
  font-size: 16px;
  color: #18181B;
}

.content_filter {

}

.category {
  .text {
    font-size: 14px;
  }
}

.content_time {
  .text {
    font-size: 14px;
  }

  .slider {
    height: 50px;
    margin-left: 15px;
    margin-right: 15px;
  }

  .input_wrapper {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }

  .time_input {
    width: 70px;
  }
}
</style>
