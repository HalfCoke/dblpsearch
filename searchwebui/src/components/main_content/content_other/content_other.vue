<template>
  <div class="content_other">
    <!--    <div class="text">-->
    <!--      <p>最近搜索</p>-->
    <!--    </div>-->
    <!--    <div class="recent_search_word">-->
    <!--      <p>...</p>-->
    <!--    </div>-->
    <div class="text">
      <p>最多搜索</p>
    </div>
    <div class="most_search_word">
      <vue-word-cloud
              class="tag_cloud"
              :words="most_search_word"
              :color="([, weight]) => weight > 5 ? '#1f77b4' : weight > 2 ? '#629fc9' : '#94bedb'"
              :font-size-ratio="10"
              :spacing="3"
              font-family="Roboto"
      />
    </div>
    <div class="beian">
      <div class="icp">
        <a target="_blank" href="http://beian.miit.gov.cn">京 ICP 备 2020039820 号 - 1</a>
      </div>
      <div class="gongan">
        <a class="gongan_link"
           target="_blank"
           href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802033291">
          <img src="https://gitee.com/halfcoke/blog_img/raw/master/img/gongAn.png" alt=""/>
          京公网安备 11010802033291 号
        </a>
      </div>
    </div>
    <div class="contact_wrapper">
		  <span class="contact"
                @click="showContact">
			与我联系
		  </span>
      © 2021 HalfCoke
    </div>
    <el-drawer
            title="联系方式"
            :visible.sync="drawer"
            :direction="direction"
    >
      <div class="contact_content">
        <div class="email">
          <span>邮箱：halfcoke@163.com</span>
        </div>
        <div class="blog">
          博客：<a href="https://halfcoke.github.io/">https://halfcoke.github.io</a>
        </div>
        <div class="wx_public">
          公众号：微信搜索 “世颜” 或 “half_640”
          <div class="qrcode">
            <img src="https://gitee.com/halfcoke/blog_img/raw/master/img/sin_qrcode.png"
                 alt="qrcode">
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import VueWordCloud from 'vuewordcloud';
import { request } from "@/requests";

export default {
  name: "content_other",
  data () {
    return {
      drawer: false,
      direction: 'rtl',
      most_search_word: [],
      recent_search_word: [],
    }
  },
  created () {
    this.getKeyWord()
    setInterval(this.getKeyWord, 10000)
  },
  methods: {
    showContact () {
      this.drawer = true
    },
    getKeyWord () {
      let data = {
        'top_k': 50,
        'recent_k': 10
      }
      request({
        url: '/api/v1/getkeyword',
        method: "post",
        header: {
          'Content-Type': 'application/json'
        },
        data
      }).then((res) => {
        this.most_search_word = []
        let map = new Map()
        for (let word of res.data.most_search_word) {
          if (word[0].length > 40 || word[0].indexOf("\\") !== -1) {
          } else {
            for (let w of word[0].split(/\W/)) {
              if (map.has(w)) {
                let count = map.get(w) + word[1]
                map.set(w, count)
              } else {
                map.set(w, word[1])
              }
            }
          }
        }
        console.log(map)
        for (let [k, v] of map) {
          this.most_search_word.push([k, v])
        }
        this.recent_search_word = res.data.recent_search_word
      })
    }
  },
  components: {
    VueWordCloud,
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

.beian {
  a {
    text-decoration: none;
    color: #859dc2;
    font-size: 13px;
    height: 26px;

    &:hover {
      color: #175199;
    }
  }

  .gongan {
    .gongan_link {
      display: inline-flex;
      align-items: center;
    }

    img {
      margin-right: 4px;
    }
  }
}

.contact_wrapper {
  font-size: 13px;
  color: #859dc2;

  .contact:hover {
    color: #175199;
  }

  .contact {
    cursor: pointer;
  }
}

.contact_content {
  color: #72767b;
  padding: 0 20px 20px;
  font-size: 13px;

  a {
    text-decoration: none;
    color: #72767b;
  }

  .email, .blog {
    margin-bottom: 20px;
  }

  .wx_public {
    .qrcode {
      display: flex;
      justify-content: center;

      img {
        display: block;
        width: 35%;
      }
    }
  }
}

.most_search_word {
  height: 160px;
  width: 100%;
}

.tag_cloud {
  height: 100%;
  width: 100%;
}
</style>
