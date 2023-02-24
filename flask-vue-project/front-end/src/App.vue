<script setup>
import axios from 'axios'
import {reactive, ref, onMounted} from "vue";
import { ElMessageBox } from 'element-plus';

//show device
const devices = reactive([])
const get_devices = () =>{
  axios.get("http://localhost:5000/devices",).then(res => {
    devices.splice(0, devices.length)
    devices.push(...res.data.results)
    console.log('Update Data')
  })
}

onMounted(() => {
  get_devices()
})

const handle_delete = (index, scope) => {
  console.log(index, scope)
  axios.delete(`http://localhost:5000/devices/${scope.device_id}`).then(() => {
    get_devices()
  })
}

//add device
const add_dialog_visible = ref(false)
const rule_form_ref = ref()
const device_form = reactive({
  device_id: "",
  device_name: "",
  user_id: "",
  device_temperature: "",
  device_humidity: "",
})

const submit_form = (formEl) => {
  axios.post('http://localhost:5000/devices', device_form).then(() => {
    add_dialog_visible.value = false
    formEl.resetFields()
    get_devices()
  })
}

const reset_form = (formEl) => {
  formEl.resetFields()
}

const handle_close = (done) => {
  ElMessageBox.confirm('Confirm Close?').then(() => {
    done();
  }).catch(() => {
  });

//edit device
const edit_form_ref = ref()
const edit_dialog_visible = ref(false)
const handle_edit = (index, scope) => {
  for (let key in scope) {
    device_form[key] = scope[key]
  }
  edit_dialog_visible.value = true
}

const submit_edit_form = (formEl) => {
  axios.put('http://localhost:5000/devices/${device_form.device_id}', device_form).then((res) => {
    formEl.resetFields()
    edit_dialog_visible.value = false
    get_devices()
  })
}

}
</script>

<template>
  <div style="margin: 0 auto; width: 100%">
    <h1 style="text-align: center">Device Management</h1>
    <!--Add Button-->
    <el-button type="primary" @click="add_dialog_visible=true" size="small">Add Device</el-button>
    <!--Show Table-->
    <el-table :data="devices" style="margin: 20px auto;">
      <el-table-column label="Device ID" prop="device_id" width="200px"/>
      <el-table-column label="Device Name" prop="device_name" width="200px"/>
      <el-table-column label="User ID" prop="user_id" width="200px"/>
      <el-table-column label="Device Temperature" prop="device_temperature" width="200px"/>
      <el-table-column label="Device Humidity" prop="device_humidity" width="200px"/>
      <el-table-column align="right" lable="Operation" width="200px">
        <template #default="scope">
          <el-button size="small" @click="handle_edit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handle_delete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <!--Add Device-->
  <el-dialog title="Add Devices" v-model="add_dialog_visible" width="30%" :before-close="handle_close">
    <el-form ref="rule_form_ref" :model="device_form" status-icon label-width="120px" class="demo-ruleForm">
      <el-form-item label="Device ID" prop="device_id">
        <el-input v-model="device_form.device_id" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Name" prop="device_name">
        <el-input v-model="device_form.device_name" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="User ID" prop="user_id">
        <el-input v-model="device_form.user_id" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Temperature" prop="device_temperature">
        <el-input v-model="device_form.device_temperature" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Humidity" prop="device_humidity">
        <el-input v-model="device_form.device_humidity" autocomplete="off"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit_form(rule_form_ref)">Submit</el-button>
        <el-button @click="reset_form(rule_form_ref)">Reset</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <!--Edit Device-->
  <el-dialog title="Edit" v-model="edit_dialog_visible" width="30%" :before-close="handle_close">
    <el-form ref="edit_form_ref" :model="device_form" status-icon label-width="120px" class="demo-ruleForm">
      <el-form-item label="Device ID" prop="device_id">
        <el-input v-model="device_form.device_id" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Name" prop="device_name">
        <el-input v-model="device_form.device_name" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="User ID" prop="user_id">
        <el-input v-model="device_form.user_id" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Temperature" prop="device_temperature">
        <el-input v-model="device_form.device_temperature" autocomplete="off"/>
      </el-form-item>
      <el-form-item label="Device Humidity" prop="device_humidity">
        <el-input v-model="device_form.device_humidity" autocomplete="off"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit_edit_form(edit_form_ref)">Submit</el-button>
        <el-button @click="reset_form(edit_form_ref)">Reset</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
