// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // 或者你实际使用的 ^0.8.x 版本

contract MockOracle {
    mapping(uint256 => uint256) public assetValues; // assetId => value

    // 模拟 Oracle 更新数据，这会消耗 Gas
    function updateAssetValue(uint256 assetId, uint256 newValue) public {
        // 模拟一些计算或验证工作
        uint256 temp = 0;
        for(uint i = 0; i < 10; i++){ // 消耗一点 gas
            temp += i;
        }
        // 使用 temp 来避免 "unused variable" 警告，同时确保操作有副作用
        assetValues[assetId] = newValue + temp - temp;
    }

    // 模拟合约读取 Oracle 数据 (这里直接读取状态，真实 Oracle 可能更复杂)
    function getAssetValue(uint256 assetId) public view returns (uint256) {
        return assetValues[assetId];
    }
}