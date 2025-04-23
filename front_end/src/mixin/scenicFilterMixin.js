import axios from 'axios';
export default {
    data() {
        return {
            scenicFilters: [],
        };
    },
    mounted() {
        
        this.fetchScenicFilters(); // 获取标签过滤器选项
    },
    methods: {
        fetchScenicFilters() {
            axios.get('http://localhost:8000/api/scenic/')
                .then(response => {
                    this.scenicFilters = response.data.map(scenic => ({
                        text: scenic.scenic_name,
                        value: scenic.scenic_id,
                    }));
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        filterTag(value, row) {
            return row.scenic == value; // 根据过滤器的值来过滤表格数据
        },
        getTagType(category) {
            // 根据 scenicName 返回相应的标签类型
            if (category == '1') {
                return 'success';
            } else if (category == '2') {
                return 'danger';
            } else if (category == '4') {
                return 'warning';
            }
            return 'primary';
        },
        setTagName(scenic) {
            if (scenic == '1') {
                return '西湖';
            } else if (scenic == '2') {
                return '西溪湿地';
            } else if (scenic == '3') {
                return '千岛湖';
            } else if (scenic == '4') {
                return '良渚古城';
            }
            return '大明山';
        },
    },
};