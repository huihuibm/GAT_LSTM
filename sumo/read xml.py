import matplotlib.pyplot as plt



data = [0.782341,0.234568,0.21345,0.456789,0.567890,0.345678,0.876543,0.987654,0.123456]
data1=[0.123456,0.456789,0.321098,0.234567,0.12345,0.345678,0.210987]
data1=[0.987654,0.789012,0.678901,0.890123,0.765432,0.123456,0.456789,0.321098,0.234567,0.12345,0.345678,0.210987,0.7243210,0.707890]


# 生成横坐标编号，从0开始
x_labels = range(1, len(data1) + 1)

# 绘制柱状图
bars = plt.bar(x_labels, data1)

# 设置坐标轴标签
plt.xlabel('Road_id')
plt.ylabel('Percentage of Travel Speed\nImprovement in the Road Network')

# 设置y轴范围，确保能完整显示底部的x标签
plt.yticks([i / 10 for i in range(1, 11)], [f'{i / 10:.1f}' for i in range(1, 11)])  # 假设y轴最大值比数据最大值大10

# 在每个柱状图上方显示对应的数字
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height,
             f'{height:.2f}',
             ha='center', va='bottom')


# 设置x轴的刻度标签
plt.xticks(x_labels, [str(i) for i in x_labels])  # 将x_labels转换为字符串列表作为刻度标签

# 显示图表
plt.show()
