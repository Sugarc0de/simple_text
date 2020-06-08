<template>
  <div>
    <el-button size="small" type="primary"><i class="el-icon-upload el-icon-right"></i>
      <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      <!--<button v-on:click="submitFile()">Submit</button>-->
    </el-button>
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
        file: '',
        import_text: false
      }
    },

    methods: {
      /*
        Submits the file to the server
      */
      async submitFile(){
        /*
                Initialize the form data
            */
            let formData = new FormData();

            /*
                Add the form data we need to submit
            */
            formData.append('file', this.file);

        /*
          Make the request to the POST /ocr URL
        */
            try {
              const response = await axios.post('/app/ocr',
                formData,
                {
                  headers: {
                    'Content-Type': 'multipart/form-data'
                  }
                }
              );
              this.$store.commit('save_file', this.file);
              this.$store.commit('save_ocr', response['data']['ocr_results']);

            } catch(e) {
              this.errors.push(e)
            };
            this.$router.push('/ocr_result')
      },

      /*
        Handles a change on the file upload
      */
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
        this.submitFile()
      }
    }
  }
</script>


<style scoped>
input[type=file]{
  color:transparent;
  width: 80px;
  font-size: 10px;
}
</style>
