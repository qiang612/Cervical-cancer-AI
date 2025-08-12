import axios from '@/utils/axios';

/**
 * 获取数据集列表
 * @returns {Promise} 包含数据集列表的Promise
 */
export function getDatasets() {
  return axios.get('/api/datasets')
    .then(response => response.data);
}

/**
 * 创建新数据集
 * @param {Object} dataset - 数据集信息
 * @returns {Promise} 包含新创建数据集的Promise
 */
export function createDataset(dataset) {
  return axios.post('/api/datasets', dataset)
    .then(response => response.data);
}

/**
 * 更新数据集信息
 * @param {string} datasetId - 数据集ID
 * @param {Object} dataset - 要更新的数据集信息
 * @returns {Promise} 包含更新后数据集的Promise
 */
export function updateDataset(datasetId, dataset) {
  return axios.put(`/api/datasets/${datasetId}`, dataset)
    .then(response => response.data);
}

/**
 * 获取数据集详情
 * @param {string} datasetId - 数据集ID
 * @returns {Promise} 包含数据集详情的Promise
 */
export function getDatasetDetails(datasetId) {
  return axios.get(`/api/datasets/${datasetId}`)
    .then(response => response.data);
}

/**
 * 删除数据集
 * @param {string} datasetId - 数据集ID
 * @returns {Promise} 包含删除结果的Promise
 */
export function deleteDataset(datasetId) {
  return axios.delete(`/api/datasets/${datasetId}`)
    .then(response => response.data);
}

/**
 * 复制数据集
 * @param {string} datasetId - 数据集ID
 * @returns {Promise} 包含复制后新数据集的Promise
 */
export function copyDataset(datasetId) {
  // Post请求的第二个参数是body，这里没有body，所以传null
  return axios.post(`/api/datasets/${datasetId}/copy`, null)
    .then(response => response.data);
}

/**
 * 迁移数据集（改变任务类型）
 * @param {string} datasetId - 数据集ID
 * @param {Object} params - 迁移参数，包含新任务类型和新名称
 * @returns {Promise} 包含迁移后新数据集的Promise
 */
export function moveDataset(datasetId, params) {
  return axios.post(`/api/datasets/${datasetId}/move`, params)
    .then(response => response.data);
}

/**
 * 分享数据集
 * @param {string} datasetId - 数据集ID
 * @param {Object} params - 分享参数，包含目标用户ID和权限
 * @returns {Promise} 包含分享结果的Promise
 */
export function shareDataset(datasetId, params) {
  return axios.post(`/api/datasets/${datasetId}/share`, params)
    .then(response => response.data);
}

/**
 * 删除数据集中的图片
 * @param {string} datasetId - 数据集ID
 * @param {string} imageId - 图片ID
 * @returns {Promise} 包含删除结果的Promise
 */
export function deleteImage(datasetId, imageId) {
  return axios.delete(`/api/datasets/${datasetId}/images/${imageId}`)
    .then(response => response.data);
}

/**
 * 搜索用户（用于分享功能）
 * @param {string} query - 搜索关键词
 * @returns {Promise} 包含搜索结果的Promise
 */
export function searchUsers(query) {
  return axios.get(`/api/users?search=${encodeURIComponent(query)}`)
    .then(response => response.data);
}
