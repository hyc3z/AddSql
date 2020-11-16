<template>
    <div>
                <el-card shadow="hover" style="height:777px;">
                    <div class="el-page-header__title" style="width: 100%; height: 200%; text-align: center; margin-bottom: 20px">
                            <h2>销售内容<br/></h2>
                        </div>
                 <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
            >
                <el-table-column prop="skillname" label="技能名" align="center"></el-table-column>
                <el-table-column prop="level" label="等级" align="center"></el-table-column>
                <el-table-column prop="nexp" label="目前经验" align="center"></el-table-column>
                <el-table-column prop="reexp" label="升级所需经验" align="center"></el-table-column>
<!--                <el-table-column label="操作" width="180" align="center">-->
<!--                    <template slot-scope="scope">-->
<!--                        <el-button-->
<!--                            type="text"-->
<!--                            icon="el-icon-edit"-->
<!--                            @click="handleEdit(scope.$index, scope.row)"-->
<!--                        >编辑</el-button>-->
<!--                        <el-button-->
<!--                            type="text"-->
<!--                            icon="el-icon-delete"-->
<!--                            class="red"-->
<!--                            @click="handleDelete(scope.$index, scope.row)"-->
<!--                        >删除</el-button>-->
<!--                    </template>-->
<!--                </el-table-column>-->
            </el-table>
          </el-card>
    </div>
</template>