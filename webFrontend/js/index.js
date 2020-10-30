popUp = new Vue({
  el: '.pop_up',
  data: {
    res_cata_data: {keys: [], paper_titles: {}, res_len: -1},
    activeClass: -1,
    activePopUp: -1,
  },
  methods: {
    item_click: function (index) {
      if (this.activeClass === index) {
        this.activeClass = -1
      } else {
        this.activeClass = index;
      }
    },
    close_popUp: function () {
      this.activePopUp = -1;
    }
  }
})


total_vue = new Vue({
  el: '.search_and_res',
  data: {
    keys: '',
    yf: '--Select start year--',
    yt: '--Select end year--',
    cata: [],
    year: _get_year()
  },
  methods: {
    get_res: function () {
      params = {
        keys: this.keys,
        yf: this.yf,
        yt: this.yt,
        category: this.cata,
      }
      _get_res(params)
      popUp.activePopUp = 1
      popUp.res_cata_data.res_len = 0
    },
    show_res: function () {
      popUp.activePopUp = 1
    }

  }
})


function _get_res(params) {
  axios.post('http://www.halfcoke.cn/api/v1/search',
      params,
      {
        header: {'Content-Type': 'application/json'}
      }
  ).then(function (response) {
    popUp.res_cata_data['keys'] = response.data.keys
    popUp.res_cata_data['paper_titles'] = response.data.paper_titles
  }).catch(function (error) {
    alert("系统错误！")
    console.log(error);
  })
}

function _get_year() {
  let date = new Date();
  let res = [];
  let cu_year = date.getFullYear()
  for (let i = 0; cu_year >= 1930; i++, cu_year--) {
    res[i] = cu_year
  }
  return res;
}




