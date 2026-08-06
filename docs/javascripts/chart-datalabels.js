// Custom global plugin for Chart.js to display numbers/labels on charts
if (typeof Chart !== 'undefined') {
  const customDatalabelsPlugin = {
    id: 'customDatalabels',
    afterDatasetsDraw(chart) {
      // If datalabels is explicitly disabled in chart options, skip
      if (chart.options.plugins && chart.options.plugins.datalabels === false) {
        return;
      }
      
      const { ctx } = chart;
      ctx.save();
      
      chart.data.datasets.forEach((dataset, datasetIndex) => {
        const meta = chart.getDatasetMeta(datasetIndex);
        if (meta.hidden) return;
        
        meta.data.forEach((element, index) => {
          const dataVal = dataset.data[index];
          if (dataVal === null || dataVal === undefined) return;
          
          let text = '';
          const chartType = chart.config.type;
          
          // Format based on chart type and values
          if (chartType === 'doughnut' || chartType === 'pie') {
            // Show as percentage
            text = dataVal + '%';
          } else if (chartType === 'radar') {
            // Radar values typically decimal format (e.g. 0.890)
            text = dataVal.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 3 });
          } else if (chartType === 'bar') {
            // Bar chart formatting
            const isPercentageBar = (dataset.label && dataset.label.includes('%')) ||
                                    (chart.options.scales && chart.options.scales.y && chart.options.scales.y.max === 100) ||
                                    (chart.options.scales && chart.options.scales.x && chart.options.scales.x.max === 100);
            if (isPercentageBar) {
              text = dataVal + '%';
            } else {
              text = dataVal.toLocaleString('pt-BR');
            }
          } else if (chartType === 'line') {
            // Line chart formatting
            const isPercentageLine = (dataset.label && (dataset.label.includes('%') || dataset.label.includes('Aprovação') || dataset.label.includes('Resolução')));
            if (isPercentageLine) {
              text = dataVal + '%';
            } else if (dataVal < 10) {
              text = dataVal.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 2 });
            } else {
              text = dataVal.toLocaleString('pt-BR');
            }
          } else {
            text = dataVal.toString();
          }
          
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 10px Inter, sans-serif';
          ctx.textAlign = 'center';
          
          if (chartType === 'doughnut' || chartType === 'pie') {
            ctx.textBaseline = 'middle';
            if (typeof element.getCenterPoint === 'function') {
              const { x, y } = element.getCenterPoint();
              ctx.fillText(text, x, y);
            }
          } else if (chartType === 'radar') {
            ctx.textBaseline = 'bottom';
            const x = element.x;
            const y = element.y;
            if (x !== undefined && y !== undefined) {
              ctx.fillText(text, x, y - 8);
            }
          } else if (chartType === 'bar' && chart.options.indexAxis === 'y') {
            // Horizontal bar chart
            ctx.textBaseline = 'middle';
            ctx.textAlign = 'left';
            const x = element.x;
            const y = element.y;
            if (x !== undefined && y !== undefined) {
              ctx.fillText(text, x + 6, y);
            }
          } else {
            // Vertical bar, line, etc.
            ctx.textBaseline = 'bottom';
            const x = element.x;
            const y = element.y;
            if (x !== undefined && y !== undefined) {
              ctx.fillText(text, x, y - 6);
            }
          }
        });
      });
      
      ctx.restore();
    }
  };
  
  Chart.register(customDatalabelsPlugin);
}
