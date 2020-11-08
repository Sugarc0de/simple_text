<template>
  <div>
    <el-upload action="" accept="image/jpeg,image/png" :data="fileList" :show-file-list="false" :httpRequest="submitFile" multiple :limit="1">
      <el-button size="large" type="primary">荧光识词</el-button>
    </el-upload>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    /*
      Defines the data used by the component
    */
    data(){
      return {
        fileList: {},
        import_text: false
      }
    },

    methods: {
      /*
        Submits the file to the server
      */
      submitFile(param) {
        /*
                Initialize the form data
            */
            var formData = new FormData();

            /*
                Add the form data we need to submit
            */
            formData.append('file', param.file);

        /*
          Make the request to the POST /ocr URL
        */
            let self = this
            axios({
              method: 'post',
              url: '/app/ocr',
              data: formData,
              headers: {
                'Content-Type': 'multipart/form-data',
              }
            }).then(function (response) {
              console.log(`response is ${response['data']}`);
              self.$store.commit('save_file', param.file);
              self.$store.commit('save_ocr', response['data']['ocr_results']);
            }).catch(function (error) {
              console.log(error)
            }).then(function () {
               self.$router.push('/ocr_result')
            });
      }
    }
  }
</script>

<style scoped>
.el-button {
  font-size: 18px;
  border: 3px solid white;
  background-color: Transparent;
}
</style>
