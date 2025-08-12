<template>
  <div class="data-preparation-container">
    <div class="top-bar">
      <div class="search-container">
        <el-input
          v-model="datasetSearchQuery"
          placeholder="搜索数据集..."
          prefix-icon="Search"
          class="dataset-search"
          @input="filterDatasets"
        />
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" @click="showCreateDatasetDialog = true">
          <el-icon><Plus /></el-icon> 创建数据集
        </el-button>
        <el-button type="default" @click="refreshDatasets">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
      </div>
    </div>

    <div class="main-content">
      <div class="filter-panel">
        <h3>筛选条件</h3>
        
        <el-form :model="filterForm" class="filter-form">
          <el-form-item label="任务类型">
            <el-select
              v-model="filterForm.taskType"
              placeholder="全部"
              @change="filterDatasets"
              style="width: 100%;"
            >
              <el-option label="全部" value="" />
              <el-option label="目标检测" value="detection" />
              <el-option label="图像分类" value="classification" />
              <el-option label="语义分割" value="segmentation" />
              <el-option label="姿态估计" value="pose" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="影像类型">
            <el-select
              v-model="filterForm.imageType"
              placeholder="全部"
              @change="filterDatasets"
              style="width: 100%;"
            >
              <el-option label="全部" value="" />
              <el-option label="X光片" value="xray" />
              <el-option label="CT扫描" value="ct" />
              <el-option label="病理切片" value="pathology" />
              <el-option label="超声图像" value="ultrasound" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="访问权限">
            <el-select
              v-model="filterForm.accessType"
              placeholder="全部"
              @change="filterDatasets"
              style="width: 100%;"
            >
              <el-option label="全部" value="" />
              <el-option label="我的数据集" value="my" />
              <el-option label="共享给我" value="shared" />
            </el-select>
          </el-form-item>
        </el-form>
        
        <div class="dataset-stats">
          <p>总计: {{ filteredDatasets.length }} 个数据集</p>
          <p>图像总数: {{ totalImages }} 张</p>
        </div>
      </div>
      
      <div class="content-area">
        <div v-if="!currentDataset" class="dataset-list">
          <div v-if="filteredDatasets.length === 0" class="empty-state">
            <el-empty description="没有找到匹配的数据集" />
          </div>
          
          <div v-else class="dataset-grid">
            <div 
              v-for="dataset in filteredDatasets" 
              :key="dataset.id" 
              class="dataset-card"
              @click="enterDataset(dataset)"
            >
              <div class="dataset-icon">
                <el-icon><FolderOpened /></el-icon>
              </div>
              <div class="dataset-info">
                <h4 class="dataset-name">{{ dataset.name }}</h4>
                <p class="dataset-meta">
                  {{ dataset.image_count }} 张图片 | 
                  {{ formatTaskType(dataset.taskType) }} |
                  {{ formatDate(dataset.created_at) }}
                </p>
              </div>
              <div class="dataset-actions">
                <el-dropdown @command="handleDatasetAction($event, dataset)" @click.stop>
                  <el-button icon="More" circle />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="copy">复制</el-dropdown-item>
                      <el-dropdown-item command="move">迁移</el-dropdown-item>
                      <el-dropdown-item command="share">分享</el-dropdown-item>
                      <el-dropdown-item command="delete" class="text-red-500">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="currentDataset" class="dataset-detail">
          <div class="dataset-detail-header">
            <el-button @click="leaveDataset" :icon="ArrowLeft">
               返回数据集列表
            </el-button>
            <h2 class="dataset-detail-title">{{ currentDataset.name }}</h2>
            <div class="dataset-detail-actions">
              <el-button @click="showUploadImagesDialog = true" :icon="Upload">
                上传图片
              </el-button>
              <el-button @click="openEditDialog(currentDataset)" :icon="Edit">
                编辑信息
              </el-button>
            </div>
          </div>
          
          <div class="dataset-detail-info">
            <div class="dataset-detail-meta">
              <p><strong>任务类型:</strong> {{ formatTaskType(currentDataset.taskType) }}</p>
              <p><strong>影像类型:</strong> {{ formatImageType(currentDataset.imageType) }}</p>
              <p><strong>创建时间:</strong> {{ formatDate(currentDataset.created_at) }}</p>
              <p><strong>最后修改:</strong> {{ formatDate(currentDataset.updated_at) }}</p>
              <p><strong>创建者:</strong> {{ currentDataset.owner?.username || '未知' }}</p>
              <p><strong>共享给:</strong> {{ currentDataset.sharedWith?.length || 0 }} 位用户</p>
            </div>
            <div class="dataset-detail-description">
              <h4>描述</h4>
              <p>{{ currentDataset.description || '无描述信息' }}</p>
            </div>
          </div>
          
          <div class="dataset-images-header">
            <h3>图片列表 ({{ currentDataset.images?.length || 0 }})</h3>
            <div class="image-filter-controls">
              <el-input
                v-model="imageSearchQuery"
                placeholder="搜索图片..."
                prefix-icon="Search"
                class="image-search"
              />
              <el-select
                v-model="imageFormatFilter"
                placeholder="图片格式"
                class="image-format-filter"
                clearable
              >
                <el-option label="全部格式" value="" />
                <el-option label="JPG" value="jpg" />
                <el-option label="PNG" value="png" />
                <el-option label="TIFF" value="tiff" />
                <el-option label="DICOM" value="dcm" />
              </el-select>
            </div>
          </div>
          
          <div class="image-grid">
            <div v-if="filteredImages.length === 0" class="empty-state">
              <el-empty description="没有找到匹配的图片" />
            </div>
            
            <div 
              v-else
              v-for="image in filteredImages" 
              :key="image.id" 
              class="image-card"
            >
              <div class="image-container">
                <img :src="image.file_path" :alt="image.filename" class="dataset-image" />
                <div class="image-overlay">
                  <el-button 
                    icon="Delete" 
                    circle 
                    type="danger" 
                    size="small"
                    @click.stop="confirmDeleteImage(image.id)"
                  />
                </div>
              </div>
              <div class="image-info">
                <p class="image-name">{{ image.filename }}</p>
                <p class="image-meta">{{ formatFileSize(image.size) }} | {{ image.format?.toUpperCase() }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog 
      title="创建新数据集" 
      v-model="showCreateDatasetDialog" 
      :before-close="handleCloseCreateDialog"
      width="500px"
    >
      <el-form :model="newDataset" :rules="datasetRules" ref="createDatasetFormRef" label-position="top">
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="newDataset.name" placeholder="请输入数据集名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="taskType">
          <el-select v-model="newDataset.taskType" placeholder="请选择任务类型" style="width: 100%;">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="影像类型" prop="imageType">
          <el-select v-model="newDataset.imageType" placeholder="请选择影像类型" style="width: 100%;">
            <el-option label="X光片" value="xray" />
            <el-option label="CT扫描" value="ct" />
            <el-option label="病理切片" value="pathology" />
            <el-option label="超声图像" value="ultrasound" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="newDataset.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入数据集的描述信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCloseCreateDialog">取消</el-button>
        <el-button type="primary" @click="handleCreateDataset">创建</el-button>
      </template>
    </el-dialog>

    <el-dialog 
      title="上传图片到数据集" 
      v-model="showUploadImagesDialog"
      width="600px"
      v-if="currentDataset"
    >
      <el-upload
        class="upload-demo"
        drag
        :action="`/api/datasets/${currentDataset.id}/images`"
        multiple
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :file-list="uploadFileList"
        :headers="{ Authorization: `Bearer ${token}` }"
      >
        <el-icon class="el-icon--upload"><Upload /></el-icon>
        <div class="el-upload__text">
          拖放文件到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip text-center">
            支持 JPG, PNG, TIFF, DICOM 等格式，单文件不超过 10MB
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadImagesDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-dialog 
      title="编辑数据集信息" 
      v-model="showDatasetEditDialog"
      width="500px"
      v-if="editDataset"
    >
      <el-form :model="editDataset" :rules="datasetRules" ref="editDatasetFormRef" label-position="top">
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="editDataset.name" />
        </el-form-item>
        <el-form-item label="任务类型" prop="taskType">
          <el-select v-model="editDataset.taskType" style="width: 100%;">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="影像类型" prop="imageType">
          <el-select v-model="editDataset.imageType" style="width: 100%;">
            <el-option label="X光片" value="xray" />
            <el-option label="CT扫描" value="ct" />
            <el-option label="病理切片" value="pathology" />
            <el-option label="超声图像" value="ultrasound" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="editDataset.description" 
            type="textarea" 
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDatasetEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateDataset">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog 
      title="分享数据集" 
      v-model="showShareDatasetDialog"
      width="500px"
      v-if="sharingDataset"
    >
      <p>将数据集 "{{ sharingDataset.name }}" 分享给其他用户</p>
      <el-form :model="shareForm" class="mt-4" label-position="top">
        <el-form-item label="用户">
          <el-select
            v-model="shareForm.userId"
            filterable
            remote
            :remote-method="searchUsers"
            :loading="isSearchingUsers"
            placeholder="搜索用户名"
            style="width: 100%;"
          >
            <el-option
              v-for="user in searchUsersResult"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权限">
          <el-radio-group v-model="shareForm.permission">
            <el-radio label="view">仅查看</el-radio>
            <el-radio label="edit">可编辑</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showShareDatasetDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmShare">确认分享</el-button>
      </template>
    </el-dialog>

    <el-dialog 
      title="迁移数据集" 
      v-model="showMoveDatasetDialog"
      width="500px"
      v-if="movingDataset"
    >
      <p>将数据集 "{{ movingDataset.name }}" 迁移为新的任务类型</p>
      <el-form :model="moveForm" class="mt-4" label-position="top">
        <el-form-item label="新任务类型" prop="newTaskType">
          <el-select v-model="moveForm.newTaskType" placeholder="请选择新的任务类型" style="width: 100%;">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="新数据集名称">
          <el-input 
            v-model="moveForm.newName" 
            :placeholder="`${movingDataset.name}_${moveForm.newTaskType}`"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMoveDatasetDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmMoveDataset">确认迁移</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { formatDate, formatFileSize, formatTaskType, formatImageType } from '@/utils/formatters';
import { useStore } from 'vuex';
import * as datasetApi from '@/api/dataset';

// 引入Element Plus图标
import { 
  Search, Plus, Refresh, FolderOpened, More, ArrowLeft, 
  Upload, Edit, Delete 
} from '@element-plus/icons-vue';

// --- Vuex and Auth ---
const store = useStore();
const token = computed(() => store.state.user.token);

// --- Form Refs ---
const createDatasetFormRef = ref(null);
const editDatasetFormRef = ref(null);

// --- Datasets State ---
const datasets = ref([]);
const filteredDatasets = ref([]);
const currentDataset = ref(null);
const datasetSearchQuery = ref('');

// --- Filter Form ---
const filterForm = reactive({
  taskType: '',
  imageType: '',
  accessType: 'my' // 默认只看自己的
});

// --- Create Dataset Dialog ---
const showCreateDatasetDialog = ref(false);
const newDataset = reactive({
  name: '',
  taskType: 'detection',
  imageType: 'pathology',
  description: ''
});

// --- Edit Dataset Dialog ---
const showDatasetEditDialog = ref(false);
const editDataset = ref(null);

// --- Validation Rules ---
const datasetRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { max: 50, message: '名称不能超过50个字符', trigger: 'blur' }
  ],
  taskType: [
    { required: true, message: '请选择任务类型', trigger: 'change' }
  ],
  imageType: [
    { required: true, message: '请选择影像类型', trigger: 'change' }
  ]
};

// --- Upload Images Dialog ---
const showUploadImagesDialog = ref(false);
const uploadFileList = ref([]);

// --- Share Dataset Dialog ---
const showShareDatasetDialog = ref(false);
const shareForm = reactive({
  userId: '',
  permission: 'view'
});
const searchUsersResult = ref([]);
const isSearchingUsers = ref(false);
const sharingDataset = ref(null);

// --- Move Dataset Dialog ---
const showMoveDatasetDialog = ref(false);
const movingDataset = ref(null);
const moveForm = reactive({
  newTaskType: '',
  newName: ''
});

// --- Images State (for detail view) ---
const imageSearchQuery = ref('');
const imageFormatFilter = ref('');
const filteredImages = computed(() => {
  if (!currentDataset.value || !Array.isArray(currentDataset.value.images)) return [];
  
  return currentDataset.value.images.filter(image => {
    const query = imageSearchQuery.value.toLowerCase();
    const format = imageFormatFilter.value;
    const matchesSearch = image.filename.toLowerCase().includes(query);
    const matchesFormat = format ? image.format === format : true;
    return matchesSearch && matchesFormat;
  });
});

// --- Computed Stats ---
const totalImages = computed(() => {
  return datasets.value.reduce((sum, dataset) => sum + (dataset.image_count || 0), 0);
});

// --- Lifecycle Hook ---
onMounted(() => {
  fetchDatasets();
});

// --- API Call Functions ---

const fetchDatasets = async () => {
  try {
    const response = await datasetApi.getDatasets();
    datasets.value = response;
    filterDatasets();
  } catch (error) {
    ElMessage.error('获取数据集失败: ' + (error.response?.data?.msg || error.message));
  }
};

const handleCreateDataset = async () => {
  if (!createDatasetFormRef.value) return;
  await createDatasetFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        console.log("创建数据集参数:", newDataset); // 打印参数用于调试
        const response = await datasetApi.createDataset(newDataset);
        // ... 成功处理
      } catch (error) {
        console.error("创建数据集错误详情:", error.response); // 打印完整错误响应
        ElMessage.error('创建数据集失败: ' + (error.response?.data?.msg || error.message));
      }
    }
  });
};

const handleUpdateDataset = async () => {
  if (!editDatasetFormRef.value) return;
  await editDatasetFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await datasetApi.updateDataset(editDataset.value.id, editDataset.value);
        
        const index = datasets.value.findIndex(d => d.id === editDataset.value.id);
        if (index !== -1) {
          datasets.value[index] = response;
        }
        
        if (currentDataset.value && currentDataset.value.id === editDataset.value.id) {
          currentDataset.value = response;
        }

        filterDatasets();
        showDatasetEditDialog.value = false;
        ElMessage.success('数据集更新成功');
      } catch (error) {
        ElMessage.error('更新数据集失败: ' + (error.response?.data?.msg || error.message));
      }
    }
  });
};

const handleDeleteDataset = async (datasetId) => {
  try {
    await datasetApi.deleteDataset(datasetId);
    datasets.value = datasets.value.filter(dataset => dataset.id !== datasetId);
    
    if (currentDataset.value && currentDataset.value.id === datasetId) {
      currentDataset.value = null;
    }
    filterDatasets();
    ElMessage.success('数据集删除成功');
  } catch (error) {
    ElMessage.error('删除数据集失败: ' + (error.response?.data?.msg || error.message));
  }
};

const handleCopyDataset = async (datasetId) => {
  try {
    const response = await datasetApi.copyDataset(datasetId);
    datasets.value.unshift(response);
    filterDatasets();
    ElMessage.success('数据集复制成功');
  } catch (error) {
    ElMessage.error('复制数据集失败: ' + (error.response?.data?.msg || error.message));
  }
};

const confirmMoveDataset = async () => {
  if (!movingDataset.value) return;
  const { id } = movingDataset.value;
  try {
    const response = await datasetApi.moveDataset(id, moveForm);
    datasets.value.unshift(response);
    filterDatasets();
    showMoveDatasetDialog.value = false;
    ElMessage.success('数据集迁移成功');
  } catch (error) {
    ElMessage.error('迁移数据集失败: ' + (error.response?.data?.msg || error.message));
  }
};

const confirmShare = async () => {
  if (!sharingDataset.value || !shareForm.userId) {
    ElMessage.warning('请选择要分享的用户');
    return;
  }
  const { id } = sharingDataset.value;
  try {
    await datasetApi.shareDataset(id, shareForm);
    showShareDatasetDialog.value = false;
    ElMessage.success('数据集分享成功');
    
    if (currentDataset.value && currentDataset.value.id === id) {
      fetchDatasetDetails(id);
    }
  } catch (error) {
    ElMessage.error('分享数据集失败: ' + (error.response?.data?.msg || error.message));
  }
};

const fetchDatasetDetails = async (datasetId) => {
  try {
    const response = await datasetApi.getDatasetDetails(datasetId);
    currentDataset.value = response;
  } catch (error) {
    ElMessage.error('获取数据集详情失败: ' + (error.response?.data?.msg || error.message));
    currentDataset.value = null; // 获取失败时清空
  }
};

const handleDeleteImage = async (imageId) => {
  if (!currentDataset.value) return;
  const datasetId = currentDataset.value.id;

  try {
    await datasetApi.deleteImage(datasetId, imageId);
    
    if (currentDataset.value.images) {
      currentDataset.value.images = currentDataset.value.images.filter(
        image => image.id !== imageId
      );
      currentDataset.value.image_count = currentDataset.value.images.length;
    }
    ElMessage.success('图片删除成功');
  } catch (error) {
    ElMessage.error('删除图片失败: ' + (error.response?.data?.msg || error.message));
  }
};

const searchUsers = async (query) => {
  if (!query.trim()) {
    searchUsersResult.value = [];
    return;
  }
  
  isSearchingUsers.value = true;
  try {
    const response = await datasetApi.searchUsers(query);
    searchUsersResult.value = response;
  } catch (error) {
    searchUsersResult.value = [];
    console.error('搜索用户失败:', error);
  } finally {
    isSearchingUsers.value = false;
  }
};

// --- Event Handlers & UI Logic ---

const filterDatasets = () => {
  filteredDatasets.value = datasets.value.filter(dataset => {
    const matchesSearch = dataset.name.toLowerCase().includes(datasetSearchQuery.value.toLowerCase());
    const matchesTaskType = filterForm.taskType ? dataset.taskType === filterForm.taskType : true;
    const matchesImageType = filterForm.imageType ? dataset.imageType === filterForm.imageType : true;
    
    // 注意：后端需要在 GET /datasets 的返回中为每个数据集提供 isOwner 字段
    let matchesAccessType = true;
    if (filterForm.accessType === 'my') {
        matchesAccessType = dataset.isOwner === true;
    } else if (filterForm.accessType === 'shared') {
        matchesAccessType = dataset.isOwner === false;
    }
    
    return matchesSearch && matchesTaskType && matchesImageType && matchesAccessType;
  });
};

const enterDataset = (dataset) => {
  fetchDatasetDetails(dataset.id);
};

const leaveDataset = () => {
  currentDataset.value = null;
  imageSearchQuery.value = '';
  imageFormatFilter.value = '';
};

const refreshDatasets = () => {
  ElMessage.info('正在刷新...');
  fetchDatasets();
};

const handleDatasetAction = (action, dataset) => {
  switch (action) {
    case 'edit':
      openEditDialog(dataset);
      break;
    case 'copy':
      handleCopyDataset(dataset.id);
      break;
    case 'move':
      movingDataset.value = dataset;
      moveForm.newTaskType = dataset.taskType;
      moveForm.newName = '';
      showMoveDatasetDialog.value = true;
      break;
    case 'share':
      sharingDataset.value = dataset;
      shareForm.userId = '';
      shareForm.permission = 'view';
      searchUsersResult.value = [];
      showShareDatasetDialog.value = true;
      break;
    case 'delete':
      confirmDeleteDataset(dataset);
      break;
  }
};

const openEditDialog = (dataset) => {
  editDataset.value = { ...dataset };
  showDatasetEditDialog.value = true;
};

const confirmDeleteDataset = (dataset) => {
  ElMessageBox.confirm(
    `确定要删除数据集 "${dataset.name}" 吗？此操作不可撤销。`,
    '确认删除',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    handleDeleteDataset(dataset.id);
  });
};

const confirmDeleteImage = (imageId) => {
  ElMessageBox.confirm(
    `确定要删除这张图片吗？`,
    '确认删除',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
      center: true,
    }
  ).then(() => {
    handleDeleteImage(imageId);
  });
};

const handleUploadSuccess = (response, uploadFile, uploadFiles) => {
  ElMessage.success(`${uploadFile.name} 上传成功`);
  if (uploadFiles.every(file => file.status === 'success')) {
      uploadFileList.value = []; 
      if (currentDataset.value) {
        fetchDatasetDetails(currentDataset.value.id);
      }
  }
};

const handleUploadError = (error, uploadFile) => {
    const err = JSON.parse(error.message);
    ElMessage.error(`${uploadFile.name} 上传失败: ${err.msg || '未知错误'}`);
};

const handleCloseCreateDialog = () => {
  if (createDatasetFormRef.value) {
    createDatasetFormRef.value.resetFields();
  }
  // 手动重置非表单prop绑定的字段
  newDataset.description = ''; 
  showCreateDatasetDialog.value = false;
};
</script>

<style scoped>
.data-preparation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.search-container {
  width: 300px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.filter-panel {
  width: 260px;
  background-color: #fff;
  padding: 20px;
  border-right: 1px solid #e5e7eb;
  overflow-y: auto;
  flex-shrink: 0;
}

.filter-panel h3 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 16px;
  color: #1f2937;
}

.filter-form .el-form-item {
  margin-bottom: 20px;
}

.dataset-stats {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
  font-size: 14px;
}
.dataset-stats p {
    margin: 8px 0;
}

.content-area {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.dataset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.dataset-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.dataset-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.dataset-icon {
  font-size: 32px;
  color: #409eff;
  margin-right: 16px;
}

.dataset-info {
  flex: 1;
  overflow: hidden;
}

.dataset-name {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #303133;
}

.dataset-meta {
  font-size: 12px;
  color: #909399;
  margin: 0;
  white-space: nowrap;
}

.dataset-actions {
  margin-left: 16px;
}

.dataset-detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.dataset-detail-title {
  margin: 0;
  font-size: 24px;
  color: #1f2937;
  flex-grow: 1;
}

.dataset-detail-info {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 32px;
  margin-bottom: 24px;
  padding: 24px;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.dataset-detail-meta p {
  margin: 0 0 12px 0;
  color: #606266;
  font-size: 14px;
}
.dataset-detail-meta p:last-child {
    margin-bottom: 0;
}
.dataset-detail-meta strong {
    color: #303133;
    margin-right: 8px;
}

.dataset-detail-description h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 16px;
}

.dataset-detail-description p {
  color: #606266;
  line-height: 1.6;
}

.dataset-images-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.image-filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.image-search {
  width: 200px;
}

.image-format-filter {
  width: 140px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.image-card {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  position: relative;
}
.image-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.image-container {
  width: 100%;
  padding-top: 100%;
  position: relative;
  background-color: #f5f7fa;
}

.dataset-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.image-card:hover .image-overlay {
  opacity: 1;
}

.image-info {
  padding: 12px;
  background-color: #fff;
}

.image-name {
  margin: 0 0 4px 0;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #303133;
}

.image-meta {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  border: 1px dashed #dcdfe6;
}

.mt-4 {
    margin-top: 16px;
}
.text-red-500 {
    color: #f56c6c;
}
</style>