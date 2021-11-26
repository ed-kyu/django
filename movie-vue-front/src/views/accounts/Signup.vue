<template>
<div class="container d-flex justify-content-center mt-3 signup-box">
  <div class="mt-3 d-flex flex-column justify-content-center signup-form">
    <div class="form-group d-flex my-3 align-items-center">
      <label class="signup-text" for="username">Username</label>
      <input 
        type="text" 
        id="username"
        minlength="1"
        maxlength="10"
        v-model="credentials.username"
        class="form-control mx-3" placeholder="Enter Username" required
      >
    </div>
    <div class="form-group d-flex my-3 align-items-center">
      <label class="signup-text" for="password">Password</label>
      <input 
        type="password" 
        id="password"
        v-model="credentials.password"
        class="form-control mx-3" placeholder="Password" required
      >
    </div>
    <div class="form-group d-flex my-3 align-items-center">
      <label for="passwordConfirmation" class="signup-text">Password Confirmation</label>
      <input 
        type="password" 
        id="passwordConfirmation"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
        class="form-control mx-3" placeholder="Password Confirmation" required
      >
    </div>
    <button @click="signup" class="btn btn-primary my-3">Signup</button>
  </div>
</div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
        passwordConfirmation: null,
      },
    }
  },
  methods: {
    signup: function () {
      axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/signup/`,
        data: this.credentials
      })
        .then(() => {
          // console.log(res)
          this.$router.push({ name: 'Login'})
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>
body {
  height: 100vh;
}
.signup-box{
  background-image: url('~@/assets/login2.png');
  background-repeat : no-repeat;
  background-size : cover;
  /* border: 1px solid black; */
  /* border-radius: 20px; */
  width: 50rem;
  height: 30rem;
  position: relative;
  top: 120px;
  border-radius: 5%;
  opacity: 1;
}
.signup-form{
  position: relative;
  left: 70px;
}
.signup-text {
  color: white;
}
</style>