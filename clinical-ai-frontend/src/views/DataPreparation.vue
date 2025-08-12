<template>
  <div class="data-preparation-container">
    <!-- 顶部操作栏 -->
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
          <el-icon-plus /> 创建数据集
        </el-button>
        <el-button type="default" @click="refreshDatasets">
          <el-icon-refresh /> 刷新
        </el-button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧筛选面板 -->
      <div class="filter-panel">
        <h3>筛选条件</h3>
        
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="任务类型">
            <el-select
              v-model="filterForm.taskType"
              placeholder="全部"
              @change="filterDatasets"
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
      
      <!-- 右侧内容区 -->
      <div class="content-area">
        <!-- 数据集列表视图 -->
        <div v-if="!currentDataset" class="dataset-list">
          <div v-if="filteredDatasets.length === 0" class="empty-state">
            <el-empty description="没有找到匹配的数据集" />
          </div>
          
          <div class="dataset-grid">
            <div 
              v-for="dataset in filteredDatasets" 
              :key="dataset.id" 
              class="dataset-card"
              @click="enterDataset(dataset)"
            >
              <div class="dataset-icon">
                <el-icon-folder-opened />
              </div>
              <div class="dataset-info">
                <h4 class="dataset-name">{{ dataset.name }}</h4>
                <p class="dataset-meta">
                  {{ dataset.imageCount }} 张图片 | 
                  {{ dataset.taskType | formatTaskType }} |
                  {{ formatDate(dataset.createdAt) }}
                </p>
              </div>
              <div class="dataset-actions">
                <el-dropdown @command="handleDatasetAction($event, dataset)">
                  <el-button icon="More" circle />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="copy">复制</el-dropdown-item>
                      <el-dropdown-item command="move">迁移</el-dropdown-item>
                      <el-dropdown-item command="share">分享</el-dropdown-item>
                      <el-dropdown-item command="delete" danger>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 数据集详情视图 -->
        <div v-if="currentDataset" class="dataset-detail">
          <div class="dataset-detail-header">
            <el-button @click="leaveDataset">
              <el-icon-arrow-left /> 返回数据集列表
            </el-button>
            <h2 class="dataset-detail-title">{{ currentDataset.name }}</h2>
            <div class="dataset-detail-actions">
              <el-button @click="showUploadImagesDialog = true">
                <el-icon-upload /> 上传图片
              </el-button>
              <el-button @click="showDatasetEditDialog = true">
                <el-icon-edit /> 编辑信息
              </el-button>
            </div>
          </div>
          
          <div class="dataset-detail-info">
            <div class="dataset-detail-meta">
              <p><strong>任务类型:</strong> {{ currentDataset.taskType | formatTaskType }}</p>
              <p><strong>影像类型:</strong> {{ currentDataset.imageType | formatImageType }}</p>
              <p><strong>创建时间:</strong> {{ formatDate(currentDataset.createdAt) }}</p>
              <p><strong>最后修改:</strong> {{ formatDate(currentDataset.updatedAt) }}</p>
              <p><strong>创建者:</strong> {{ currentDataset.creator }}</p>
              <p><strong>共享给:</strong> {{ currentDataset.sharedUsers.length }} 位用户</p>
            </div>
            <div class="dataset-detail-description">
              <h4>描述</h4>
              <p>{{ currentDataset.description || '无描述信息' }}</p>
            </div>
          </div>
          
          <div class="dataset-images-header">
            <h3>图片列表 ({{ currentDataset.images.length }})</h3>
            <div class="image-filter-controls">
              <el-input
                v-model="imageSearchQuery"
                placeholder="搜索图片..."
                prefix-icon="Search"
                class="image-search"
                @input="filterImages"
              />
              <el-select
                v-model="imageFormatFilter"
                placeholder="图片格式"
                @change="filterImages"
                class="image-format-filter"
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
              v-for="image in filteredImages" 
              :key="image.id" 
              class="image-card"
            >
              <div class="image-container">
                <img :src="image.url" :alt="image.name" class="dataset-image" />
                <div class="image-overlay">
                  <el-button 
                    icon="Delete" 
                    circle 
                    type="danger" 
                    size="small"
                    @click.stop="deleteImage(image.id)"
                  />
                </div>
              </div>
              <div class="image-info">
                <p class="image-name">{{ image.name }}</p>
                <p class="image-meta">{{ image.size | formatFileSize }} | {{ image.format.toUpperCase() }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建数据集对话框 -->
    <el-dialog 
      title="创建新数据集" 
      v-model="showCreateDatasetDialog" 
      :before-close="handleCloseCreateDialog"
    >
      <el-form :model="newDataset" :rules="datasetRules" ref="datasetForm">
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="newDataset.name" />
        </el-form-item>
        <el-form-item label="任务类型" prop="taskType">
          <el-select v-model="newDataset.taskType">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="影像类型" prop="imageType">
          <el-select v-model="newDataset.imageType">
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
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDatasetDialog = false">取消</el-button>
        <el-button type="primary" @click="createDataset">创建</el-button>
      </template>
    </el-dialog>

    <!-- 上传图片对话框 -->
    <el-dialog 
      title="上传图片到数据集" 
      v-model="showUploadImagesDialog"
      width="600px"
    >
      <el-upload
        class="upload-demo"
        drag
        :action="`/api/datasets/${currentDataset.id}/images`"
        multiple
        :on-success="handleUploadSuccess"
        :file-list="uploadFileList"
        :headers="{ Authorization: `Bearer ${token}` }"
      >
        <el-icon-upload />
        <div class="el-upload__text">
          拖放文件到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip text-center">
            支持 JPG、PNG、TIFF、DICOM 等格式，单文件不超过10MB
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadImagesDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 编辑数据集对话框 -->
    <el-dialog 
      title="编辑数据集" 
      v-model="showDatasetEditDialog"
    >
      <el-form :model="editDataset" :rules="datasetRules" ref="editDatasetForm">
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="editDataset.name" />
        </el-form-item>
        <el-form-item label="任务类型" prop="taskType">
          <el-select v-model="editDataset.taskType">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="影像类型" prop="imageType">
          <el-select v-model="editDataset.imageType">
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
        <el-button type="primary" @click="saveDatasetEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 分享数据集对话框 -->
    <el-dialog 
      title="分享数据集" 
      v-model="showShareDatasetDialog"
    >
      <el-form :model="shareForm">
        <el-form-item label="用户">
          <el-select
            v-model="shareForm.userId"
            filterable
            remote
            :remote-method="searchUsers"
            placeholder="搜索用户"
          >
            <el-option
              v-for="user in searchUsersResult"
              :key="user.id"
              :label="user.name"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权限">
          <el-radio-group v-model="shareForm.permission">
            <el-radio label="view">仅查看</el-radio>
            <el-radio label="edit">可编辑</el-radio>
            <el-radio label="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showShareDatasetDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmShare">确认分享</el-button>
      </template>
    </el-dialog>

    <!-- 数据集迁移对话框 -->
    <el-dialog 
      title="迁移数据集" 
      v-model="showMoveDatasetDialog"
    >
      <p>将数据集 "{{ movingDataset?.name }}" 迁移为新的任务类型</p>
      <el-form :model="moveForm">
        <el-form-item label="新任务类型" prop="newTaskType">
          <el-select v-model="moveForm.newTaskType">
            <el-option label="目标检测" value="detection" />
            <el-option label="图像分类" value="classification" />
            <el-option label="语义分割" value="segmentation" />
            <el-option label="姿态估计" value="pose" />
          </el-select>
        </el-form-item>
        <el-form-item label="新数据集名称">
          <el-input 
            v-model="moveForm.newName" 
            :placeholder="`${movingDataset?.name}_${moveForm.newTaskType}`"
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
import { ElMessage, ElMessageBox, ElEmpty } from 'element-plus';
import { formatDate, formatFileSize, formatTaskType, formatImageType } from '@/utils/formatters';
import { useStore } from 'vuex';
import * as datasetApi from '@/api/dataset';

// 引入Element Plus图标
import { 
  Search, Plus, Refresh, FolderOpened, More, ArrowLeft, 
  Upload, Edit, Delete 
} from '@element-plus/icons-vue';

// 状态管理
const store = useStore();
const token = computed(() => store.state.user.token);

// 数据集相关状态
const datasets = ref([]);
const filteredDatasets = ref([]);
const currentDataset = ref(null);
const datasetSearchQuery = ref('');

// 筛选表单
const filterForm = reactive({
  taskType: '',
  imageType: '',
  accessType: ''
});

// 创建数据集对话框
const showCreateDatasetDialog = ref(false);
const newDataset = reactive({
  name: '',
  taskType: 'detection',
  imageType: 'pathology',
  description: ''
});

// 编辑数据集对话框
const showDatasetEditDialog = ref(false);
const editDataset = ref({});

// 数据集验证规则
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

// 上传图片相关
const showUploadImagesDialog = ref(false);
const uploadFileList = ref([]);

// 分享数据集相关
const showShareDatasetDialog = ref(false);
const shareForm = reactive({
  userId: '',
  permission: 'view'
});
const searchUsersResult = ref([]);
const sharingDataset = ref(null);

// 迁移数据集相关
const showMoveDatasetDialog = ref(false);
const movingDataset = ref(null);
const moveForm = reactive({
  newTaskType: '',
  newName: ''
});

// 图片筛选相关
const imageSearchQuery = ref('');
const imageFormatFilter = ref('');
const filteredImages = computed(() => {
  if (!currentDataset.value) return [];
  
  return currentDataset.value.images.filter(image => {
    const matchesSearch = image.name.toLowerCase().includes(imageSearchQuery.value.toLowerCase());
    const matchesFormat = imageFormatFilter.value ? image.format === imageFormatFilter.value : true;
    return matchesSearch && matchesFormat;
  });
});

// 统计信息
const totalImages = computed(() => {
  return datasets.value.reduce((sum, dataset) => sum + dataset.imageCount, 0);
});

// 生命周期钩子
onMounted(() => {
  fetchDatasets();
});

// API 调用函数
const fetchDatasets = async () => {
  try {
    const response = await datasetApi.getDatasets();
    datasets.value = response;
    filterDatasets();
  } catch (error) {
    ElMessage.error('获取数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const createDataset = async () => {
  try {
    const response = await datasetApi.createDataset(newDataset);
    datasets.value.push(response);
    showCreateDatasetDialog.value = false;
    ElMessage.success('数据集创建成功');
    // 重置表单
    newDataset.name = '';
    newDataset.description = '';
    filterDatasets();
  } catch (error) {
    ElMessage.error('创建数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const updateDataset = async () => {
  try {
    const response = await datasetApi.updateDataset(editDataset.value.id, editDataset.value);
    // 更新数据集列表中的对应项
    const index = datasets.value.findIndex(d => d.id === editDataset.value.id);
    if (index !== -1) {
      datasets.value[index] = response;
    }
    // 如果正在查看该数据集，也更新当前视图
    if (currentDataset.value && currentDataset.value.id === editDataset.value.id) {
      currentDataset.value = response;
    }
    showDatasetEditDialog.value = false;
    ElMessage.success('数据集更新成功');
    filterDatasets();
  } catch (error) {
    ElMessage.error('更新数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const deleteDataset = async (datasetId) => {
  try {
    await datasetApi.deleteDataset(datasetId);
    datasets.value = datasets.value.filter(dataset => dataset.id !== datasetId);
    // 如果删除的是当前查看的数据集，返回列表视图
    if (currentDataset.value && currentDataset.value.id === datasetId) {
      currentDataset.value = null;
    }
    ElMessage.success('数据集删除成功');
    filterDatasets();
  } catch (error) {
    ElMessage.error('删除数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const copyDataset = async (datasetId) => {
  try {
    const response = await datasetApi.copyDataset(datasetId);
    datasets.value.push(response);
    ElMessage.success('数据集复制成功');
    filterDatasets();
  } catch (error) {
    ElMessage.error('复制数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const moveDataset = async (datasetId) => {
  try {
    const response = await datasetApi.moveDataset(datasetId, {
      newTaskType: moveForm.newTaskType,
      newName: moveForm.newName
    });
    datasets.value.push(response);
    showMoveDatasetDialog.value = false;
    ElMessage.success('数据集迁移成功');
    filterDatasets();
  } catch (error) {
    ElMessage.error('迁移数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const shareDataset = async (datasetId) => {
  try {
    await datasetApi.shareDataset(datasetId, {
      userId: shareForm.userId,
      permission: shareForm.permission
    });
    showShareDatasetDialog.value = false;
    ElMessage.success('数据集分享成功');
    // 更新当前数据集信息
    if (currentDataset.value && currentDataset.value.id === datasetId) {
      fetchDatasetDetails(datasetId);
    }
  } catch (error) {
    ElMessage.error('分享数据集失败: ' + (error.response?.data?.message || error.message));
  }
};

const fetchDatasetDetails = async (datasetId) => {
  try {
    const response = await datasetApi.getDatasetDetails(datasetId);
    currentDataset.value = response;
  } catch (error) {
    ElMessage.error('获取数据集详情失败: ' + (error.response?.data?.message || error.message));
  }
};

const deleteImage = async (imageId) => {
  if (!currentDataset.value) return;
  
  try {
    await datasetApi.deleteImage(currentDataset.value.id, imageId);
    currentDataset.value.images = currentDataset.value.images.filter(
      image => image.id !== imageId
    );
    currentDataset.value.imageCount = currentDataset.value.images.length;
    ElMessage.success('图片删除成功');
  } catch (error) {
    ElMessage.error('删除图片失败: ' + (error.response?.data?.message || error.message));
  }
};

const searchUsers = async (query) => {
  if (!query) {
    searchUsersResult.value = [];
    return;
  }
  
  try {
    const response = await datasetApi.searchUsers(query);
    searchUsersResult.value = response;
  } catch (error) {
    ElMessage.error('搜索用户失败: ' + (error.response?.data?.message || error.message));
  }
};

// 事件处理函数
const filterDatasets = () => {
  filteredDatasets.value = datasets.value.filter(dataset => {
    const matchesSearch = dataset.name.toLowerCase().includes(datasetSearchQuery.value.toLowerCase());
    const matchesTaskType = filterForm.taskType ? dataset.taskType === filterForm.taskType : true;
    const matchesImageType = filterForm.imageType ? dataset.imageType === filterForm.imageType : true;
    const matchesAccessType = filterForm.accessType 
      ? (filterForm.accessType === 'my' && dataset.isOwner) || 
        (filterForm.accessType === 'shared' && !dataset.isOwner && dataset.shared)
      : true;
    
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
  fetchDatasets();
  if (currentDataset.value) {
    fetchDatasetDetails(currentDataset.value.id);
  }
};

const handleDatasetAction = (action, dataset) => {
  switch (action) {
    case 'edit':
      // 编辑数据集逻辑
      showDatasetEditDialog.value = true;
      editDataset.value = { ...dataset };
      break;
    case 'copy':
      copyDataset(dataset.id);
      break;
    case 'move':
      movingDataset.value = dataset;
      moveForm.newTaskType = '';
      moveForm.newName = '';
      showMoveDatasetDialog.value = true;
      break;
    case 'share':
      sharingDataset.value = dataset;
      shareForm.userId = '';
      shareForm.permission = 'view';
      showShareDatasetDialog.value = true;
      break;
    case 'delete':
      ElMessageBox.confirm(
        `确定要删除数据集"${dataset.name}"吗？此操作不可撤销。`,
        '确认删除',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        deleteDataset(dataset.id);
      });
      break;
  }
};

const handleUploadSuccess = (response) => {
  ElMessage.success('图片上传成功');
  // 刷新当前数据集图片
  if (currentDataset.value) {
    fetchDatasetDetails(currentDataset.value.id);
  }
};

const handleCloseCreateDialog = () => {
  // 重置表单
  newDataset.name = '';
  newDataset.description = '';
};

const confirmShare = () => {
  if (sharingDataset.value) {
    shareDataset(sharingDataset.value.id);
  }
};

const confirmMoveDataset = () => {
  if (movingDataset.value) {
    moveDataset(movingDataset.value.id);
  }
};

const saveDatasetEdit = () => {
  updateDataset();
};
</script>

<style scoped>
.data-preparation-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f5f7fa;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.search-container {
  width: 300px;
}

.dataset-search {
  width: 100%;
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
}

.filter-panel h3 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #1f2937;
}

.filter-form {
  margin-bottom: 24px;
}

.el-form-item {
  margin-bottom: 16px;
}

.dataset-stats {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
}

.content-area {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.dataset-list {
  height: 100%;
}

.dataset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.dataset-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.dataset-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.dataset-icon {
  font-size: 24px;
  color: #4096ff;
  margin-bottom: 12px;
}

.dataset-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dataset-meta {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

.dataset-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.dataset-detail {
  height: 100%;
}

.dataset-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.dataset-detail-title {
  margin: 0;
  font-size: 20px;
  color: #1f2937;
}

.dataset-detail-actions {
  display: flex;
  gap: 12px;
}

.dataset-detail-info {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dataset-detail-meta {
  flex: 1;
}

.dataset-detail-meta p {
  margin: 8px 0;
  color: #4b5563;
}

.dataset-detail-description {
  flex: 2;
}

.dataset-detail-description h4 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 16px;
}

.dataset-detail-description p {
  color: #4b5563;
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
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.image-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.image-container {
  position: relative;
  height: 140px;
  overflow: hidden;
}

.dataset-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-container:hover .dataset-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.image-info {
  padding: 12px;
}

.image-name {
  margin: 0 0 4px 0;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-meta {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  background-color: #fff;
  border-radius: 8px;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
