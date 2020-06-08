<template>
  <div class="container">
    <EntryPage />
  </div>
</template>

<script>
  import EntryPage from "../components/EntryPage";

  export default {
    components: {
      EntryPage
    }
  }
</script>

<style>
  .container {
    margin: 3%;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
  }

  body {
    background-image: url(../static/background.jpeg);
    background-position: center top;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    background-margin: 0% 0%;
    background-color: white;
  }

  .subtitle {
    font-weight: 300;
    font-size: 42px;
    color: #526488;
    word-spacing: 5px;
    padding-bottom: 15px;
  }

  .links {
    padding-top: 15px;
  }
</style>
