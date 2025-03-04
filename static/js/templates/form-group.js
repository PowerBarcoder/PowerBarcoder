export default `
<div :class="['form-group', customClass]">
    <label :for="actualInputId">
        <span :id="actualTooltipId">{{ label.endsWith(':') ? label.slice(0, -1) : label }}: <i class="fa fa-question-circle"></i></span>
        <span v-if="infoText" class="text-secondary information">
            <i>{{ infoText }}</i>
        </span>
    </label>
    <div v-if="dual" class="row">
        <div class="col">
            <input type="text" class="form-control" :class="secondaryClass" :id="actualSecondaryId" :name="actualSecondaryId" 
                   :placeholder="secondaryPlaceholder" v-model="secondaryInputValue" :disabled="secondaryDisabled" required>
        </div>
        <div class="col">
            <input type="text" class="form-control" :class="actualInputClass" :id="actualInputId" :name="actualInputName" 
                   :placeholder="placeholder" v-model="inputValue" required>
        </div>
    </div>
    <div v-else class="row">
        <div class="col-12">
            <input type="text" class="form-control" :class="actualInputClass" :id="actualInputId" :name="actualInputName" 
                   :placeholder="placeholder" v-model="inputValue" required>
        </div>
    </div>
</div>

`;
