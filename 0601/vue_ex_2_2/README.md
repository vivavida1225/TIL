# v-model 사용하기
```HTML
<input id="name" type="text" v-model="formData.name">
```
> input 에서 받은 값을 변수에 연동할 수 있다.

```javascript
    const app = createApp({
      setup() {
        const formData = ref({
          name: '',
          email: '',
          age: null,
          residence: '',
          languages: []
        })
        const onSubmit = function() {
          console.log(formData.value.name)
          console.log(formData.value.email)
          console.log(formData.value.age)
          console.log(formData.value.residence)
          formData.value.languages.forEach((language) => console.log(language))
        }
        return {
          onSubmit,
          formData,
        }
      }
    })
```
