<template>
  <div class="index">
    <div class="wrap-padding-ct">
      <p>form:{{pageData}}</p>
      <z_content v-model="pageData" :options="pageOptions"/>
    </div>
    <!--  model_update  -->
  </div>
</template>

<script>

import {deepCopy, object_set, setOptionsByKey} from "@/components/zz/z_funcs";
// Api writePlace

export default {
  name: 'index',
  components: {},
  data() {
    return {
      change_edit_visible: false,
      z_view_qr_visible: false,
      pageData: {
        queryParams:{
          pageIndex:1,
          pageSize:5,
          total:0,
        }
      },
      pageOptions: {
        'prop': 'pageData',
        'type': 'page',
        'label': '抽奖活动管理',
        'data': [],
        'options': {},
        children:[
          {
            'prop': 'queryParams',
            'type': 'form',
            'label': '',
            'data': [],
            press:this.press,
            'options': {inline:true},
            children: // fitter
          },
          {'prop': 'table_list',
            'type': 'table',
            'label': '',
            'data': [],
            'options': {loading:false,key:'table_list[0]'},
            children: // table_option
          },
          {
            prop: 'pageIndex', type: 'pagination', value: [1, 15, 30], data: [], options: {
              formatting: ['pageIndex', 'pageSize', 'total'],
              path:'queryParams.pageIndex'
            }, press: this.getDataList,
          },
        ]
      },
      previewUrl: '',
      copyQueryParams: {},

    };
  },
  async mounted() {
    await this.getDataList();
    this.copyQueryParams = deepCopy(this.pageData.queryParams);
    // this.copy_change_active_info = deepCopy(this.change_active_info)
    this.tableOperationInit();
  },
  methods: {
    tableOperationInit() {
      console.log('tableOperationInit')
      const tp = {}
      const tableOperationList = {
        默认: []
      };
      setOptionsByKey(this.pageOptions,'op[0]',{tableOperationList})
    },

    press(val) {
      if (val === 'add') {
        this.$router.push({path: 'add_or_edit', query: {}});
      } else if (val === 'search') {
        this.getDataList();

      } else if (val === 'reset') {
        this.queryParamsReset();
      }
    },
    async getDataList() {
      let temp_q = {}
      temp_q = {...temp_q, ...this.pageData.queryParams};
      setOptionsByKey(this.pageOptions,'table_list[0]',{loading: true})
      const data = await SOMEFUNCS_LIST(temp_q).catch(()=>{
        setOptionsByKey(this.pageOptions,'table_list[0]',{loading: false})
      })
      this.pageData = object_set(this.pageData,'table_list',data.list)
      // this.pageData.pageData.table_list = data.list;
      this.pageData.queryParams.total = data.total;
      setOptionsByKey(this.pageOptions,'table_list[0]',{loading: false})

      console.log('pageData',this.pageData)
    },
    queryParamsReset() {
      this.pageData.queryParams = deepCopy(this.copyQueryParams);
      this.getDataList();
    },
    changeActiveInfoReset() {
      this.change_active_info = deepCopy(this.copy_change_active_info)
    },

    async changeFinish() {
      // const temp_form = await prepareFormData(zfTemplateDataDeal(this.change_active_info));
      // await apiImsApiCommodityGroupAdd(temp_form);
      // this.$message.success('操作成功');
      // await this.getDataList()
      // this.change_edit_visible = false;
    },

    // 函数填充

  },
};
</script>

<style lang="scss" scoped>
.index {
  padding: 20px;
  background-color: rgb(240, 242, 245);
  position: relative;
  height: calc(100vh - 100px);
  overflow: auto;

  .wrap-padding-ct {
    position: relative;
    min-height: calc(100vh - 140px);
    background-color: #ffffff;
    padding: 20px;
  }
}
</style>
