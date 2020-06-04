

END = 'end'


class Operation:
    def __init__(self, segments):
        self._segments = segments


class Parser:

    states = {
        'filter': {
            '[where]': {
                '[and]': {
                    '[{integer}]': {
                        '{condition}': END
                    }
                },
                '[or]': {
                    '[{integer}]': {
                        '{condition}': END
                    }
                },
                '{condition}': END
            }
        }
    }

    def parse(self, querstring):
        operations = []
        for _key, _ in querstring.items():
            key = _key.lower()
            segments = self._segment_key(key)
            if self._validate_segments(segments):
                operation = Operation(segments)
                operations.append(operation)
        return operations

    def _segment_key(self, key):
        raw = key
        segments = []

        while raw:
            match_index = raw.find('[', 1)
            if match_index > 0:
                segments.append(raw[:match_index])
                raw = raw[match_index:]
                continue

            segments.append(raw)
            raw = ''
        return segments

    def _validate_segments(self, segments):
        segment_index = 0
        context = self.states
 
        while context != END:
            is_valid = False
            segment = segments[segment_index]

            if segment in context:
                context = context[segment]
                segment_index += 1
                continue
            
            for dynamic_segment_name, dynamic_segment_key in self._get_dynamic_segment(context):
                validator = getattr(self, f"_validate_dynamic_{dynamic_segment_name}", None)
                if validator(segment, segment_index, segments):
                    context = context[dynamic_segment_key]
                    is_valid = True
                    break

            if not is_valid:
                return False

            segment_index += 1
        return True
    
    def _get_dynamic_segment(self, context):
        dynamic_segments = []
        for key in context.keys():
            name = key[1:-1] if key.startswith('[') and key.endswith(']') else key
            if name.startswith('{') and name.endswith('}'):
                dynamic_segments.append((name[1:-1], key))
        return dynamic_segments

    def _validate_dynamic_integer(self, segment, index, segments):
        try:
            text = segment[1:-1] if segment.startswith('[') and segment.endswith(']') else segment
            int(text)
            return True
        except ValueError:
            return False

    def _validate_dynamic_condition(self, segment, index, segments):
        text = segment[1:-1] if segment.startswith('[') and segment.endswith(']') else segment
        if len(text.split('.')) == 2:
            return True
        return False
