// clinical-ai-frontend/src/views/DataPreparation.vue (主要修改部分)

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
        <!-- 数据集列表视图 -->
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
        
        <!-- 数据集详情视图 - 显示图片 -->
        <div v-if="currentDataset" class="dataset-detail">
          <div class="dataset-detail-header">
            <el-button @click="leaveDataset" :icon="ArrowLeft">
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
              
              <!-- 批量操作按钮 -->
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
                  :label="image.id"
                />
              </div>
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

    <!-- 批量上传图片对话框 -->
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
            v-model="shareForm.userId"
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
// clinical-ai-frontend/src/views/DataPreparation.vue (script部分)

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
const filteredImages = ref([]);
const selectedImages = ref([]); // 用于批量操作的图片ID数组

// --- Copy Images Dialog ---
const showCopyImagesDialog = ref(false);
const copyImagesForm = reactive({
  targetDatasetId: ''
});

// --- Computed Stats ---
const totalImages = computed(() => {
  return datasets.value.reduce((sum, dataset) => sum + (dataset.image_count || 0), 0);
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
    }
    ElMessage.success('图片删除成功');
  } catch (error) {
    ElMessage.error('删除图片失败: ' + (error.response?.data?.msg || error.message));
  }
};

// clinical-ai-frontend/src/views/DataPreparation.vue (script部分)

// ... (大部分 <script setup> 内容保持不变) ...

// 批量删除选中的图片
const confirmDeleteSelectedImages = async () => {
  if (selectedImages.value.length === 0) return;
  const countToDelete = selectedImages.value.length; // ## ADDED: 在删除前记录数量

  ElMessageBox.confirm(
    `确定要删除选中的 ${countToDelete} 张图片吗？`, // ## FIX: 使用记录的数量
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
        currentDataset.value.image_count = currentDataset.value.images.length;
      }

      selectedImages.value = [];
      ElMessage.success(`成功删除 ${countToDelete} 张图片`); // ## FIX: 使用记录的数量
    } catch (error) {
      ElMessage.error('删除图片失败: ' + (error.response?.data?.msg || error.message));
    }
  });
};

// 复制选中的图片到其他数据集
const confirmCopyImages = async () => {
  if (selectedImages.value.length === 0 || !copyImagesForm.targetDatasetId) return;
  const countToCopy = selectedImages.value.length; // ## ADDED: 在复制前记录数量

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
    ElMessage.success(`成功复制 ${countToCopy} 张图片`); // ## FIX: 使用记录的数量
    
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

// ... (其他 script 部分保持不变) ...
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
    const results = searchUsersResult.value.map(user => ({
      value: user.id,
      label: user.username
    }));
    cb(results);
  });
};

const handleUserSelect = (user) => {
  shareForm.userId = user.value;
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
      }
  }
};

const handleUploadError = (error, uploadFile) => {
  // ## FIX: 修正错误处理逻辑，以正确解析后端返回的错误信息 ##
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
/* 在DataPreparation.vue的style部分添加 */
<style scoped>
.data-preparation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-container {
  flex: 1;
  max-width: 500px;
}

.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  overflow: hidden;
}

.filter-panel {
  width: 280px;
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.content-area {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dataset-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
}

.dataset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.dataset-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.dataset-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dataset-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dataset-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
}

.dataset-images-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.image-filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.image-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  overflow-y: auto;
  padding-right: 10px;
}

.image-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.image-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.image-container {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.dataset-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-overlay {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-card:hover .image-overlay {
  opacity: 1;
}

.image-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

/* 滚动条美化 */
.dataset-list::-webkit-scrollbar,
.image-grid::-webkit-scrollbar {
  width: 6px;
}

.dataset-list::-webkit-scrollbar-track,
.image-grid::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.dataset-list::-webkit-scrollbar-thumb,
.image-grid::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.dataset-list::-webkit-scrollbar-thumb:hover,
.image-grid::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>