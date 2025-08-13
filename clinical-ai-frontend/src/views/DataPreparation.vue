<template>
  <div class="data-preparation-container">
    <!-- 合并为单一容器，包含导航和主内容 -->
    <div class="combined-container">
      <!-- 顶部导航栏 -->
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

      <!-- 主内容区 -->
      <div class="main-container">
        <!-- 左侧筛选区域 -->
        <div class="filter-section">
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
        
        <!-- 右侧内容区域 -->
        <div class="content-section">
          <!-- 数据集列表视图 -->
          <div v-if="!currentDataset" class="dataset-list-view">
            <div class="section-header">
              <h2>数据集列表</h2>
            </div>
            
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
                <!-- 还原文件夹样式 -->
                <div class="folder-icon-container">
                  <div class="folder-icon">
                    <el-icon><FolderOpened /></el-icon>
                  </div>
                </div>
                <div class="dataset-info">
                  <h4 class="dataset-name">{{ dataset.name }}</h4>
                  <p class="dataset-meta">
                    {{ dataset.imageCount }} 张图片 | 
                    {{ formatTaskType(dataset.taskType) }} |
                    {{ formatDate(dataset.createdAt) }}
                  </p>
                </div>
                <div class="dataset-actions">
                  <el-dropdown @command="handleDatasetAction($event, dataset)" @click.stop>
                    <el-button icon="More" circle />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">编辑</el-dropdown-item>
                        <el-dropdown-item command="copy">复制数据集</el-dropdown-item>
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
          
          <!-- 数据集详情视图 -->
          <div v-if="currentDataset" class="dataset-detail-view">
            <div class="section-header with-actions">
              <el-button @click="leaveDataset" :icon="ArrowLeft" class="back-button">
                  返回数据集列表
              </el-button>
              <h2 class="dataset-detail-title">{{ currentDataset.name }}</h2>
              <div class="dataset-detail-actions">
                <el-button @click="showUploadImagesDialog = true" :icon="Upload">
                  批量导入图片
                </el-button>
                <el-button @click="openEditDialog(currentDataset)" :icon="Edit">
                  编辑信息
                </el-button>
              </div>
            </div>
            
            <!-- 数据集详情信息 -->
            <div class="dataset-detail-content">
              <div class="dataset-metadata">
                <div class="dataset-meta-section">
                  <h3>基本信息</h3>
                  <p><strong>任务类型:</strong> {{ formatTaskType(currentDataset.taskType) }}</p>
                  <p><strong>影像类型:</strong> {{ formatImageType(currentDataset.imageType) }}</p>
                  <p><strong>创建时间:</strong> {{ formatDate(currentDataset.createdAt) }}</p>
                  <p><strong>最后修改:</strong> {{ formatDate(currentDataset.updatedAt) }}</p>
                  <p><strong>创建者:</strong> {{ currentDataset.owner?.username || '未知' }}</p>
                  <p><strong>共享给:</strong> {{ currentDataset.sharedWith?.length || 0 }} 位用户</p>
                </div>
                
                <div class="dataset-description-section">
                  <h3>描述</h3>
                  <p>{{ currentDataset.description || '无描述信息' }}</p>
                </div>
              </div>
              
              <!-- 图片列表区域 -->
              <div class="dataset-images-section">
                <div class="section-divider"></div>
                
                <div class="images-header">
                  <h3>图片列表 ({{ currentDataset.images?.length || 0 }})</h3>
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
                      class="image-format-filter"
                      clearable
                      @change="filterImages"
                    >
                      <el-option label="全部格式" value="" />
                      <el-option label="JPG" value="jpg" />
                      <el-option label="PNG" value="png" />
                      <el-option label="TIFF" value="tiff" />
                      <el-option label="DICOM" value="dcm" />
                    </el-select>
                    
                    <div v-if="selectedImages.length > 0" class="batch-actions">
                      <el-button 
                        type="primary" 
                        size="small"
                        @click="showCopyImagesDialog = true"
                      >
                        复制选中图片
                      </el-button>
                      <el-button 
                        type="danger" 
                        size="small"
                        @click="confirmDeleteSelectedImages"
                      >
                        删除选中图片
                      </el-button>
                    </div>
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
                    <div class="image-checkbox">
                      <el-checkbox
                        :model-value="selectedImages.includes(image.id)"
                        @change="() => handleImageSelection(image.id)"
                      />
                    </div>
                    <div class="image-container">
                      <img :src="`${BACKEND_URL}${image.filePath}`" :alt="image.filename" class="dataset-image" />
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
        </div>
      </div>
    </div>

    <!-- 创建数据集对话框 -->
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

    <!-- 批量导入图片对话框 -->
    <el-dialog
      title="批量导入图片到数据集"
      v-model="showUploadImagesDialog"
      width="600px"
      v-if="currentDataset"
    >
      <el-upload
        class="upload-demo"
        drag
        :action="`/api/datasets/${currentDataset.id}/images/batch`"
        multiple
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :file-list="uploadFileList"
        :headers="{ Authorization: `Bearer ${token}` }"
        :limit="50"
        :on-exceed="handleExceed"
      >
        <el-icon class="el-icon--upload"><Upload /></el-icon>
        <div class="el-upload__text">
          拖放文件到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip text-center">
            支持 JPG, PNG, TIFF, DICOM 等格式，单文件不超过 10MB，一次最多上传50个文件
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="showUploadImagesDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 编辑数据集对话框 -->
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

    <!-- 分享数据集对话框 -->
    <el-dialog
      title="分享数据集"
      v-model="showShareDatasetDialog"
      width="500px"
      v-if="sharingDataset"
    >
      <p>将数据集 "{{ sharingDataset.name }}" 分享给其他用户</p>
      <el-form :model="shareForm" class="mt-4" label-position="top">
        <el-form-item label="用户">
          <el-autocomplete
            v-model="userSearchText"
            :fetch-suggestions="querySearchUsers"
            placeholder="输入用户名搜索"
            :loading="isSearchingUsers"
            @select="handleUserSelect"
          />
        </el-form-item>
        <el-form-item label="权限">
          <el-select v-model="shareForm.permission" style="width: 100%;">
            <el-option label="查看" value="view" />
            <el-option label="编辑" value="edit" />
            <el-option label="管理" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showShareDatasetDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmShare">确认分享</el-button>
      </template>
    </el-dialog>

    <!-- 迁移数据集对话框 -->
    <el-dialog
      title="迁移数据集"
      v-model="showMoveDatasetDialog"
      width="500px"
      v-if="movingDataset"
    >
      <p>将数据集 "{{ movingDataset.name }}" 迁移为其他任务类型</p>
      <el-form :model="moveForm" class="mt-4" label-position="top">
        <el-form-item label="新任务类型">
          <el-select v-model="moveForm.newTaskType" style="width: 100%;">
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

    <!-- 复制图片对话框 -->
    <el-dialog
      v-if="currentDataset"
      title="复制图片到其他数据集"
      v-model="showCopyImagesDialog"
      width="500px"
    >
      <p>将 {{ selectedImages.length }} 张图片复制到:</p>
      <el-form :model="copyImagesForm" class="mt-4" label-position="top">
        <el-form-item label="目标数据集">
          <el-select
            v-model="copyImagesForm.targetDatasetId"
            style="width: 100%;"
            placeholder="选择目标数据集"
          >
            <el-option
              v-for="dataset in datasets"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
              :disabled="dataset.id === currentDataset.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCopyImagesDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmCopyImages">确认复制</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus';
import { formatDate, formatFileSize, formatTaskType, formatImageType } from '@/utils/formatters';
import { useStore } from 'vuex';
import * as datasetApi from '@/api/dataset';

// 引入Element Plus图标
import { 
  Search, Plus, Refresh, FolderOpened, More, ArrowLeft, 
  Upload, Edit, Delete, Check
} from '@element-plus/icons-vue';

const BACKEND_URL = 'http://localhost:5000';
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
const userSearchText = ref('');
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
const filteredImages = ref([]);
const selectedImages = ref([]); // 用于批量操作的图片ID数组

// --- Copy Images Dialog ---
const showCopyImagesDialog = ref(false);
const copyImagesForm = reactive({
  targetDatasetId: ''
});

// --- Computed Stats ---
const totalImages = computed(() => {
  // ## FIX: 使用正确的 camelCase 字段名 imageCount ##
  return datasets.value.reduce((sum, dataset) => sum + (dataset.imageCount || 0), 0);
});
// --- Lifecycle Hook ---
onMounted(() => {
  fetchDatasets();
});

// 监听当前数据集变化，自动筛选图片
watch(currentDataset, () => {
  filterImages();
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
        const response = await datasetApi.createDataset(newDataset);
        datasets.value.unshift(response); // 添加到列表开头
        filterDatasets();
        
        // 重置表单
        newDataset.name = '';
        newDataset.description = '';
        newDataset.taskType = 'detection';
        newDataset.imageType = 'pathology';
        
        showCreateDatasetDialog.value = false;
        ElMessage.success('数据集创建成功');
      } catch (error) {
       console.error("创建数据集错误详情:", error); 
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
        
        // 更新数据集列表
        const index = datasets.value.findIndex(d => d.id === editDataset.value.id);
        if (index !== -1) {
          datasets.value[index] = response;
        }
        
        // 更新当前查看的数据集
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
    
    // 如果删除的是当前查看的数据集，返回列表视图
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
    
    // 刷新当前数据集详情
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
    
    // 更新当前数据集的图片列表
    if (currentDataset.value.images) {
      currentDataset.value.images = currentDataset.value.images.filter(
        image => image.id !== imageId
      );
      currentDataset.value.image_count = currentDataset.value.images.length;
      
      // 从选中列表中移除
      selectedImages.value = selectedImages.value.filter(id => id !== imageId);
      filterImages();
    }
    fetchDatasets();
    ElMessage.success('图片删除成功');
  } catch (error) {
    ElMessage.error('删除图片失败: ' + (error.response?.data?.msg || error.message));
  }
};

// 批量删除选中的图片
const confirmDeleteSelectedImages = async () => {
  if (selectedImages.value.length === 0) return;
  const countToDelete = selectedImages.value.length;

  ElMessageBox.confirm(
    `确定要删除选中的 ${countToDelete} 张图片吗？`,
    '确认删除',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
      center: true,
    }
  ).then(async () => {
    if (!currentDataset.value) return;
    const datasetId = currentDataset.value.id;

    try {
      // 使用 Promise.all 并行删除以提高效率
      const deletePromises = selectedImages.value.map(imageId => 
        datasetApi.deleteImage(datasetId, imageId)
      );
      await Promise.all(deletePromises);

      // 更新图片列表
      if (currentDataset.value.images) {
        const selectedIds = new Set(selectedImages.value);
        currentDataset.value.images = currentDataset.value.images.filter(
          image => !selectedIds.has(image.id)
        );
        currentDataset.value.imageCount = currentDataset.value.images.length;
        filterImages();
      }
      fetchDatasets();
      selectedImages.value = [];
      ElMessage.success(`成功删除 ${countToDelete} 张图片`);
    } catch (error) {
      ElMessage.error('删除图片失败: ' + (error.response?.data?.msg || error.message));
    }
  });
};

// 复制选中的图片到其他数据集
const confirmCopyImages = async () => {
  if (selectedImages.value.length === 0 || !copyImagesForm.targetDatasetId) return;
  const countToCopy = selectedImages.value.length;

  try {
    await datasetApi.copyImages(
      currentDataset.value.id,
      copyImagesForm.targetDatasetId,
      selectedImages.value
    );

    showCopyImagesDialog.value = false;
    // 清空表单和选中项
    copyImagesForm.targetDatasetId = '';
    selectedImages.value = []; 
    ElMessage.success(`成功复制 ${countToCopy} 张图片`);
    
    // 提示用户是否刷新目标数据集以查看新图片
    ElNotification({
        title: '复制成功',
        message: '图片已复制到目标数据集。如果需要立即查看，请刷新页面或重新进入目标数据集。',
        type: 'success',
    });

  } catch (error) {
    ElMessage.error('复制图片失败: ' + (error.response?.data?.msg || error.message));
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

// --- 搜索用户的自动完成回调 ---
const querySearchUsers = (queryString, cb) => {
  searchUsers(queryString).then(() => {
    const results = searchUsersResult.value.map(user => {
      return {
        // ## FIX: 让 'value' 成为需要显示的用户名 ##
        value: user.username, 
        // ## ADDED: 将用户ID作为附加属性，供后续使用 ##
        id: user.id 
      };
    });
    cb(results);
  });
};

const handleUserSelect = (item) => {
   // ## FIX: 从选中项的 'id' 属性获取用户ID ##
  shareForm.userId = item.id; 
  // ## FIX: 从选中项的 'value' 属性获取用户名以更新输入框 ##
  userSearchText.value = item.value; 
};

// --- Event Handlers & UI Logic ---

const filterDatasets = () => {
  filteredDatasets.value = datasets.value.filter(dataset => {
    const matchesSearch = dataset.name.toLowerCase().includes(datasetSearchQuery.value.toLowerCase());
    const matchesTaskType = filterForm.taskType ? dataset.taskType === filterForm.taskType : true;
    const matchesImageType = filterForm.imageType ? dataset.imageType === filterForm.imageType : true;
    
    // 按访问权限筛选
    let matchesAccessType = true;
    if (filterForm.accessType === 'my') {
        matchesAccessType = dataset.isOwner === true;
    } else if (filterForm.accessType === 'shared') {
        matchesAccessType = dataset.isOwner === false;
    }
    
    return matchesSearch && matchesTaskType && matchesImageType && matchesAccessType;
  });
};

// 筛选图片
const filterImages = () => {
  if (!currentDataset.value || !Array.isArray(currentDataset.value.images)) {
    filteredImages.value = [];
    return;
  }
  
  filteredImages.value = currentDataset.value.images.filter(image => {
    const query = imageSearchQuery.value.toLowerCase();
    const format = imageFormatFilter.value;
    const matchesSearch = image.filename.toLowerCase().includes(query);
    const matchesFormat = format ? image.format === format : true;
    return matchesSearch && matchesFormat;
  });
};

const enterDataset = (dataset) => {
  fetchDatasetDetails(dataset.id);
};

const leaveDataset = () => {
  currentDataset.value = null;
  imageSearchQuery.value = '';
  imageFormatFilter.value = '';
  selectedImages.value = [];
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
      shareForm.userId = ''; // 清空ID
      shareForm.permission = 'view';
      userSearchText.value = ''; // 清空输入框文本
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
    `确定要删除数据集 "${dataset.name}" 吗？此操作不可撤销，将删除所有包含的图片。`,
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

// 处理图片选择变化
const handleImageSelection = (imageId) => {
  const index = selectedImages.value.indexOf(imageId);
  if (index > -1) {
    // 如果已存在，则移除
    selectedImages.value.splice(index, 1);
  } else {
    // 如果不存在，则添加
    selectedImages.value.push(imageId);
  }
};

// 上传相关处理函数
const handleUploadSuccess = (response, uploadFile, uploadFiles) => {
  ElMessage.success(`${uploadFile.name} 上传成功`);
  // 所有文件上传完成后刷新图片列表
  if (uploadFiles.every(file => file.status === 'success')) {
      uploadFileList.value = []; 
      if (currentDataset.value) {
        fetchDatasetDetails(currentDataset.value.id);
        fetchDatasets();
      }
  }
};

const handleUploadError = (error, uploadFile) => {
  let message = '上传失败';
  try {
    // 真实的错误信息在 error.response.data.message 中
    if (error.response && error.response.data && error.response.data.message) {
      message = error.response.data.message;
    } else if (error.message) {
      // 尝试从 error.message 中解析，作为备用方案
      const err = JSON.parse(error.message);
      message = err.msg || err.message || '未知错误';
    }
  } catch (e) {
    // 如果以上都失败，说明可能是网络中断等问题
    message = '网络错误或服务器无响应';
  }
  ElMessage.error(`${uploadFile.name} 上传失败: ${message}`);
};

const handleExceed = (files, fileList) => {
  ElMessage.warning(`每次最多只能上传50个文件，本次已忽略 ${files.length} 个文件`);
};

const handleCloseCreateDialog = () => {
  if (createDatasetFormRef.value) {
    createDatasetFormRef.value.resetFields();
  }
  showCreateDatasetDialog.value = false;
};
</script>

<style scoped>
/* 基础容器样式 */
.data-preparation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 16px;
  box-sizing: border-box;
  background-color: #f5f7fa;
  gap: 16px;
}

/* 合并导航与主内容的容器 */
.combined-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

/* 顶部导航栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0; /* 底部边框分隔 */
  box-sizing: border-box;
}

.search-container {
  flex: 1;
  max-width: 500px;
}

.dataset-search {
  transition: all 0.3s ease;
}

.dataset-search:focus-within {
  box-shadow: 0 0 0 2px rgba(55, 142, 241, 0.2);
}

.action-buttons {
  display: flex;
  gap: 12px;
}

/* 主内容区 */
.main-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧筛选区域 */
.filter-section {
  width: 280px;
  padding: 20px;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  background-color: #fcfcfd;
}

.filter-section h3 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #1f2329;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f2f5;
}

.filter-form {
  margin-bottom: 24px;
}

.filter-form .el-form-item {
  margin-bottom: 16px;
}

.dataset-stats {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px dashed #e5e7eb;
  color: #6b7280;
  font-size: 14px;
}

.dataset-stats p {
  margin: 6px 0;
}

/* 右侧内容区域 */
.content-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 区域标题样式 */
.section-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
}

.section-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2329;
}

.section-header.with-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.back-button {
  margin-right: 12px;
}

.dataset-detail-title {
  flex: 1;
  min-width: 200px;
}

.dataset-detail-actions {
  display: flex;
  gap: 12px;
}

/* 数据集列表视图 */
.dataset-list-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dataset-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4,minmax(0, 1fr)); 

  column-gap: 16px; /* 列间距（左右间距）*/
  row-gap: 16px;
  padding: 20px 20px 10px; /* 底部内边距减小，平衡视觉 */
  align-content: start;
  overflow-y: auto;
}

/* 强化数据集卡片视觉效果 - 重点修改 */
.dataset-card {
  /* 加粗边框并使用更深颜色 */
  border: 1.5px solid #c5cddb;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
  width: 100%; /* 改为100%，适配网格列宽 */
  max-width: 211px; /* 保留最大宽度限制 */
  /* 固定高度（根据内容调整合适值） */
  height: 150px;
}

.dataset-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: #378ef1; /* 左侧蓝色指示条，更明显 */
}

.dataset-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: #94a3b8; /* 悬停时边框颜色加深 */
}

.dataset-icon {
  color: #378ef1;
  font-size: 24px;
  margin-bottom: 12px;
}

.dataset-info .dataset-name {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1f2329;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dataset-info .dataset-meta {
  margin: 0;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
}

.dataset-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* 数据集详情视图 */
.dataset-detail-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dataset-detail-content {
  flex: 1;
  overflow-y: auto;
}

.dataset-metadata {
  display: flex;
  gap: 20px;
  padding: 20px;
  flex-wrap: wrap;
}

.dataset-meta-section {
  flex: 1;
  min-width: 250px;
  background-color: #f9fafb;
  padding: 16px;
  border-radius: 6px;
  border: 1px solid #f0f2f5;
}

.dataset-meta-section h3,
.dataset-description-section h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #1f2329;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f2f5;
}

.dataset-meta-section p {
  margin: 8px 0;
  font-size: 14px;
  color: #4b5563;
}

.dataset-meta-section strong {
  color: #1f2329;
}

.dataset-description-section {
  flex: 2;
  min-width: 250px;
}

.dataset-description-section p {
  margin: 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  padding: 16px;
  background-color: #f9fafb;
  border-radius: 6px;
  min-height: 60px;
  border: 1px solid #f0f2f5;
}

/* 图片列表区域 */
.dataset-images-section {
  padding: 0 20px 20px;
}

.section-divider {
  height: 1px;
  background-color: #e2e8f0;
  margin: 0 -20px 20px;
}

.images-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.images-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2329;
}

.image-filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.image-search, .image-format-filter {
  min-width: 180px;
}

/* 图片网格 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  overflow-y: auto;
  max-height: calc(100vh - 420px);
}

.image-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  background-color: #ffffff;
}

.image-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-color: #d1d5db;
}

.image-container {
  position: relative;
  height: 180px;
  overflow: hidden;
  background-color: #f9fafb;
}

.dataset-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.image-card:hover .dataset-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 0 0 0 8px;
}

.image-card:hover .image-overlay {
  opacity: 1;
}

/* 优化图片选择框样式 */
.image-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
}

:deep(.image-checkbox .el-checkbox__inner) {
  width: 18px;
  height: 18px;
  border-radius: 3px;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(.image-checkbox .el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #378ef1;
  border-color: #378ef1;
}

:deep(.image-checkbox .el-checkbox__input.is-checked .el-checkbox__inner::after) {
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
}

.image-info {
  padding: 12px;
}

.image-name {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
  color: #1f2329;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-meta {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #9ca3af;
}

.empty-state .el-empty__description {
  margin-top: 16px;
  font-size: 14px;
}

/* 滚动条美化 */
.dataset-grid::-webkit-scrollbar,
.image-grid::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.dataset-grid::-webkit-scrollbar-track,
.image-grid::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.dataset-grid::-webkit-scrollbar-thumb,
.image-grid::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.dataset-grid::-webkit-scrollbar-thumb:hover,
.image-grid::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 按钮样式优化 */
:deep(.el-button) {
  border-radius: 6px;
  transition: all 0.2s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-1px);
}

:deep(.el-button--primary) {
  background-color: #378ef1;
  border-color: #378ef1;
}

:deep(.el-button--primary:hover) {
  background-color: #2574d0;
  border-color: #2574d0;
}

/* 下拉菜单样式 */
:deep(.el-dropdown-menu) {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f2f5;
}

/* 对话框样式优化 */
:deep(.el-dialog) {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}

@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .filter-section {
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .image-grid {
    max-height: calc(100vh - 500px);
  }
}
</style>