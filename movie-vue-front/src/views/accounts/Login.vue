<template>
<div class="container d-flex justify-content-center mt-3 login-box">
  <div class="mt-3 d-flex flex-column justify-content-center login-form">
    <div class="form-group d-flex my-3 align-items-center">
      <label for="username" class="login-text">Username</label>
      <input 
        type="text" 
        id="username"
        v-model="credentials.username"
        minlength="1"
        maxlength="10"
        class="form-control mx-3" placeholder="Enter Username" required
      >
    </div>
      <small id="Help" class="form-text login-text text-muted">We'll never share your info with anyone else.</small>
    <div class="form-group d-flex my-3 align-items-center">
      <label for="password" class="login-text">Password</label>
      <input 
        type="password" 
        id="password"
        v-model="credentials.password"
        class="form-control mx-3" placeholder="Password" required
        @keyup.enter="login"
      >
    </div>
    <div class="form-check d-flex justify-content-start align-items-center">
      <!-- <input type="checkbox" class="form-check-input" id="exampleCheck1"> -->
      <!-- <label class="form-check-label mx-3" for="exampleCheck1">Check me out</label> -->
    </div>
      <button @click="login" class="btn btn-primary my-3 mx-3">Login</button>
      
  </div>
</div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      },
    }
  },
  methods: {
    login: function () {
      axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/api-token-auth/`,
        data: this.credentials,
      })
        .then(res => {
          console.log('login', res)
          localStorage.setItem('jwt', res.data.token)
          this.$emit('login')
          this.$store.dispatch('LoadUserId')
          this.$router.push({ name: 'Home' })
        })
        .catch(err => {
          alert("ID와 비밀번호를 다시 확인해주세요")
          console.log(err)
        })
    }
  },
  computed: {
    ...mapState(['authUser'])
  }
}
</script>

<style scoped>
body {
  height: 100vh;
}
.login-box {
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
.login-form{
  position: relative;
  left: 30px;
}
.login-text {
  color: white;
}
</style>