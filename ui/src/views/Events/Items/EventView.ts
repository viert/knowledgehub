import { Vue, Component, Prop } from 'vue-property-decorator'
import { AnyEvent } from '@/store/types'

@Component
export default class EventView extends Vue {
  @Prop({ type: Object, required: true }) event!: AnyEvent
}
